"""
deep data structure search and replace
======================================

This portion is pure python and has no namespace external
dependencies.

The functions :func:`deep_assignment`, :func:`deep_object`
and :func:`deep_replace` are making your programmer life much
easier for to change parts of any deeply nested data/object
structures.

.. note::
    Although these 3 functions are demonstrating the beauty
    and flexibility of Python, they can create a lot of
    side-effects and (wrongly used) even crash your
    interpreter process.

    We make no guarantees or warranties, either express
    or implied - so please use them with care!

:func:`deep_search` can be very useful for discovering
internals of the Python language/libraries or for to
debug and test your Python app.

"""
import ast

from operator import getitem
from typing import Any, Callable, List, Optional, Tuple, Type, Union

from ae.base import UNSET                                                           # type: ignore


__version__ = '0.1.0'


DeepDataType = Union[dict, list]                #: deep data structure root types
DeepDataPath = List[Tuple[Any, Any]]            #: deep data path list of tuples with object and key/attribute


def deep_assignment(obj_keys: DeepDataPath, new_value: Any):
    """ set sub-attribute/item with a mutable parent object to a new value within a deeply nested object/data structure.

    :param obj_keys:            list of (object, key) tuples identifying an element within a deeply nested data
                                structure or object hierarchy. The root of the data/object structure is the object
                                at list index 0 and the element to be changed is identified by the object and
                                key in the last list item of this argument.

                                The referenced data structure can contain immutable objects (like tuples
                                and str) which will be accordingly changed/replaced if affected/needed.

                                At least one object/element within the data structure has to be mutable,
                                else a `ValueError` will be raised.

                                If the last list item references a single character in a (immutable) string then
                                also the type of :paramref:`~deep_assignment.new_value` has to be string (in this
                                case the single character will be replaced with the string in
                                :paramref:`~deep_assignment.new_value`). If the types are not matching then
                                a `TypeError` will be raised.

    :param new_value:           value to be assigned to the element referenced by the last list item of the
                                argument in :paramref:`~deep_assignment.obj_key_path`.
    """
    obj = None

    while obj_keys:
        obj, key_or_attr = obj_keys.pop()
        if isinstance(obj, str):
            new_value = obj[:key_or_attr] + new_value + obj[key_or_attr + 1:]
            continue
        if isinstance(obj, tuple):
            obj_list = list(obj)
            obj_list[key_or_attr] = new_value
            new_value = tuple(obj_list)
            continue

        if isinstance(obj, (list, dict)):
            obj[key_or_attr] = new_value
        else:
            setattr(obj, key_or_attr, new_value)

        return

    raise ValueError(f"deep_assignment({obj_keys}, {new_value}) error: "
                     f"{obj} no mutable object" if obj else "empty path")


def deep_object(obj: Any, key_path: str, new_value: Union[Any, None] = UNSET) -> Any:
    """ determine object in a deep nested object structure and optionally assign a new value to it.

    :param obj:                 start object to search in (and its sub-objects).
    :param key_path:            composed key string containing dict keys, tuple/list/str indexes and attribute names.
                                The dot (`.`) character is identifying attribute names. `[` and `]` are enclosing
                                index values, like shown in the following examples::

                                    class AClass:
                                        str_attr_name = 'a_attr_val'
                                        dict_attr = dict(a=3)

                                    class BClass:
                                        str_attr_name = 'b_b_b_b_b'
                                        a_obj = AClass()

                                    b = BClass()
                                    assert deep_object(b, 'str_attr_name') == 'b_b_b_b_b'
                                    assert deep_object(b, 'a_obj.str_attr_name') == 'a_attr_val'
                                    assert deep_object(b, 'a_obj.dict_attr["a"]') == 3

                                key path strings for dicts can alternatively be specified without the high commas
                                (enclosing the key string), like e.g.::

                                    d = dict(a_str_key=1)
                                    assert deep_object(d, '["a_str_key"]') == 1  # with high commas returns 1
                                    assert deep_object(d, '[a_str_key]') == 1    # same result/return value

                                When the first part of the key path string is specifying an index you can also
                                leave away the opening square bracket::

                                    assert deep_object(d, 'a_str_key]') == 1     # again - the same return 1

    :param new_value:           optional new value - replacing the found object. The old value will be returned.

                                .. note::
                                    Tuples and strings that are embedding the found object will be automatically
                                    updated/replaced up in the data tree structure until a mutable object
                                    (list, dict or object) get found.

    :return:                    specified object/value (the old value if :paramref:`~deep_object.new_value` got passed)
                                or :data:`~ae.base.UNSET` if not found/exists (key path string is invalid).
    """
    if key_path[0] == '[':
        key_path = key_path[1:]       # for to support fully specified indexes (starting with a square bracket)

    obj_keys = list()
    get_func = getitem if isinstance(obj, (dict, list, str, tuple)) else getattr
    while key_path and obj != UNSET:
        idx = 0
        for char in key_path:
            if char in ('.', '[', ']'):     # == `char in '.[]'` - keep strings separate for speedup
                break
            idx += 1
        else:
            char = ""
        try:
            key = ast.literal_eval(key_path[:idx])
        except (SyntaxError, ValueError):
            key = key_path[:idx]
        obj_keys.append((obj, key))

        try:
            obj = get_func(obj, key)                                    # type: ignore
        except (AttributeError, IndexError, KeyError, ValueError):
            obj = UNSET

        if char == ']':
            idx += 1
            char = key_path[idx: idx + 1]

        if idx >= len(key_path):
            if new_value != UNSET:
                deep_assignment(obj_keys, new_value)
            break

        get_func = getitem if char == '[' else getattr
        key_path = key_path[idx + 1:]

    return obj


def deep_replace(data: DeepDataType, replace_with: Callable[[DeepDataPath, Any, Any], Any],
                 immutable_types: Tuple[Type, ...] = (tuple, ), obj_keys: Optional[DeepDataPath] = None):
    """ replace values within the passed (nested) data structure.

    :param data:                list or dict data structure for to be deep searched and replaced. Can contain any
                                combination of deep nested list/dict objects. The sub-structure-types dict and list
                                as well as the immutable types specified by :paramref:`~deep_replace.immutable_types`
                                will be recursively deep searched (top down) by passing their items one by one
                                to the function specified by :paramref:`~deep_replace.replace_with`.

    :param replace_with:        called for each item with 3 arguments (data-struct-path, key in data-structure, value),
                                and if the return value is not equal to :data:`UNSET` then it will be used for
                                to overwrite the value in the data-structure.

    :param immutable_types:     tuple of immutable iterable types which will be treated as replaceable items.
                                Each of the immutable types passed in this tuple has to be convertible to a list object.
                                By default only the items of a tuple are replaceable. For to also
                                allow the replacement of single characters in a string pass the argument value
                                `(tuple, str)` into this parameter.

    :param obj_keys:            used (internally only) for to pass the parent data-struct path in recursive calls.
    """
    if isinstance(data, dict):
        items = data.items()
    elif isinstance(data, list):
        items = enumerate(data)             # type: ignore # we treat them like dicts with the index as the key
    else:
        raise ValueError(f"deep_replace(): invalid data type {type(data)} (allowed={DeepDataType})")

    if obj_keys is None:
        obj_keys = list()

    replace_items = list()
    for key, value in items:
        obj_keys.append((data, key))
        new_value = replace_with(obj_keys, key, value)
        if new_value != UNSET:
            replace_items.append((key, new_value))
        elif isinstance(value, (dict, list)):
            deep_replace(value, replace_with, immutable_types=immutable_types, obj_keys=obj_keys)
        elif isinstance(value, immutable_types):
            type_converter = type(value)
            if type_converter is str:   # for string immutables: prevent recursion; ensure correct conversion from list
                corr_immutable_types = tuple([typ for typ in immutable_types if typ is not str])
                type_converter = lambda v: "".join(v)   # type: ignore # noqa: E731
            else:
                corr_immutable_types = immutable_types
            value = list(value)
            deep_replace(value, replace_with, immutable_types=corr_immutable_types, obj_keys=obj_keys)
            replace_items.append((key, type_converter(value)))
        obj_keys.pop()

    for key, new_value in replace_items:
        data[key] = new_value


def deep_search(obj: Any, found: Callable[[DeepDataPath, Any, Any], Any],
                skip_types: Tuple[Type, ...] = (bytes, int, float, str, type),
                skip_attr_prefix: str = '__',
                obj_keys: Optional[DeepDataPath] = None
                ) -> List[Tuple[DeepDataPath, Any, Any]]:
    """ search key and/or value within the passed (nested) object structure.

    :param obj:                 root object to start the top-down deep search from, which can contain any
                                combination of deep nested elements/objects. For each sub-element the
                                callable passed into :paramref:`~deep_replace.found` will be
                                executed. If the callable returns `True` then the data path, the key and the value
                                will stored in a tuple and added to the search result list (finally returned
                                to the caller of this function).

                                For iterable objects of type dict/tuple/list the sub-items will be searched, as well
                                as the attributes determined via the Python `dir` function. To reduce the number of
                                items/attributes to be searched use the parameters :paramref:`~deep_search.skip_types`
                                and/or :paramref:`~deep_search.skip_attr_prefix`.

    :param found:               called for each item with 3 arguments (data-struct-path, key in data-structure, value),
                                and if the return value is `True` then the data/object path, the last key and value
                                will be added as a new item to the returned list.

    :param skip_types:          tuple of types to skip from to be searched deeper (see specified default tuple in the
                                parameter declaration).

    :param skip_attr_prefix:    name prefix string for attribute(s) that has/have to be skipped from deeper search.
                                By default the attributes which names starting with double-underscore characters will
                                not deeper searched.

    :param obj_keys:            used (internally only) for to pass the parent data-struct path in recursive calls.

    :return:                    list of tuples (data-struct-path, key, value); one tuple for each found item within
                                the passed :paramref:`~deep_search.obj` argument.
    """
    if isinstance(obj, skip_types):
        return []

    if isinstance(obj, dict):
        items = obj.items()
    elif isinstance(obj, (list, tuple)):
        items = enumerate(obj)              # type: ignore # we treat tuple/lists like dicts with the index as the key
    elif isinstance(obj, str):              # only needed if str got explicitly removed from skip_types
        items = enumerate(obj)              # type: ignore # we treat str types like dicts with the index as the key
        skip_types += (str, )               # add str type skip in first deeper search for to prevent endless-recursion
    else:
        items = [(k, getattr(obj, k)) for k in dir(obj) if not k.startswith(skip_attr_prefix)]  # type: ignore

    if obj_keys is None:
        obj_keys = list()

    found_items = list()
    for key, value in items:
        obj_keys.append((obj, key))
        if found(obj_keys, key, value):
            found_items.append((obj_keys.copy(), key, value))
        found_items.extend(
            deep_search(value, found, skip_types=skip_types, skip_attr_prefix=skip_attr_prefix, obj_keys=obj_keys))
        obj_keys.pop()

    return found_items


"""
Returns a named tuple which can be set using default values

taken from
http://stackoverflow.com/questions/11351032/named-tuple-and-optional-keyword-arguments

>>> Node = namedtuple_with_defaults('Node', 'val left right')
>>> Node()
Node(val=None, left=None, right=None)
>>> Node = namedtuple_with_defaults('Node', 'val left right', [1, 2, 3])
>>> Node()
Node(val=1, left=2, right=3)
>>> Node = namedtuple_with_defaults('Node', 'val left right', {'right':7})
>>> Node()
Node(val=None, left=None, right=7)
>>> Node(4)
Node(val=4, left=None, right=7)
"""

from collections import namedtuple, Mapping


def namedtuple_with_defaults(typename, field_names, default_values=()):
    my_tuple = namedtuple(typename, field_names)
    my_tuple.__new__.__defaults__ = (None,) * len(my_tuple._fields)
    if isinstance(default_values, Mapping):
        prototype = my_tuple(**default_values)
    else:
        prototype = my_tuple(*default_values)
    my_tuple.__new__.__defaults__ = tuple(prototype)
    return my_tuple

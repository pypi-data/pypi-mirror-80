#!/usr/bin/env python

## Standard Lib
from collections import OrderedDict
from inspect import Parameter, Signature

## TTILS:
from .terrors import NodeError

__all__ = ['Node']

class MetaNode(type):

    def __new__(cls, clsname, bases, clsdict):
        if len(bases) > 1:
            raise NodeError("Inheritance hierarchy unclear creating class:", clsname)
        clsobj = super().__new__(cls,clsname, bases, clsdict)

        sig = Signature([Parameter(fname, Parameter.POSITIONAL_OR_KEYWORD)
                         for fname in clsobj._fields])
        setattr(clsobj, '__signature__', sig)
        return clsobj


class Node(metaclass=MetaNode):  
    _fields = []

    def __init__(self, *args, **kwargs):
        bound_args = self.__signature__.bind(*args, **kwargs)
        for name, val in bound_args.arguments.items():
            setattr(self, name, val)

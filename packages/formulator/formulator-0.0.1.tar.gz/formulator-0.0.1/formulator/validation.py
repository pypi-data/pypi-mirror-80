#!/usr/bin/env python

## Standard Lib
from collections import OrderedDict
import logging
import re

## TTILS:
from .terrors import *
# from .ferry import *

def export(code):
    globals()[code.__name__] = code
    __all__.append(code.__name__)
    return code

__all__ = []

# class ValidatorMeta(type):

#     @classmethod
#     def __prepare__(cls, name, bases, **kwds):
#         return OrderedDict()

#     def __new__(cls, clsname, bases, clsdict):
#         fields = [key for key, val in clsdict.items()
#                   if isinstance(val, Descriptor)]
        
#         for name in fields:
#             clsdict[name].name = name
#         clsobj = super().__new__(cls, clsname, bases, dict(clsdict))
# metaclass = ValidatorMeta

class Descriptor:
    def __init__(self, name=None):
        self.name = name
    
    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            logging.debug(f"Get attribute {self.name}")
            return instance.__dict__[self.name]
    
    def __set__(self, instance, value):
        logging.debug(f"Set {self.name} {value}")
        instance.__dict__[self.name] = value
    
    def __delete__(self, instance):
        logging.debug(f"Delete {self.name}", )
        del instance.__dict__[self.name]

class Typed(Descriptor):
    
    #expected type
    ty = object

    def __set__(self, instance, value):
        if not isinstance(value, self.ty):
            raise TypeError(f"Expected {self.ty}")
        else:
            super().__set__(instance, value)

#### Base Field Types
@export
class IntField(Typed):
    ty = int


@export
class FloatField(Typed):
    ty = float


@export
class StringField(Typed):
    ty = str

#### Base Field Properties
@export
class Negative(Descriptor):
    def __set__(self, instance, value):
        if value > 0:
            raise FieldValidationError("Negative value required.")
        super().__set__(instance, value)


@export
class NonNegative(Descriptor):
    def __set__(self, instance, value):
        if value < 0:
            raise FieldValidationError("Non-negative value required.")
        super().__set__(instance, value)


@export
class Positive(Descriptor):
    def __set__(self, instance, value):
        if value <= 0:
            raise FieldValidationError("Positive value required.")
        super().__set__(instance, value)


@export
class Sized(Descriptor):
    def __init__(self, *args, maxlen, **kwargs):
        self.maxlen = maxlen
        super().__init__(*args, **kwargs)

    def __set__(self, instance, value):
        if len(value) > self.maxlen:
            raise FieldValidationError(f"Field must be smaller than length {self.maxlen}" )
        super().__set__(instance, value)


@export
class Regex(Descriptor):
    def __init__(self, *args, pattern, **kwargs):
        self.pattern = re.compile(pattern)
        super().__init__(*args, **kwargs)

    def __set__(self, instance, value):
        if not self.pattern.match(value):
            raise FieldValidationError("Invalid string value")
        super().__set__(instance, value)

#### Composite Fields
@export
class NegativeInteger(FloatField, Negative):
    pass


@export
class NonNegativeInteger(FloatField, NonNegative):
    pass


@export
class PositiveInteger(FloatField, Positive):
    pass


@export
class NegativeInteger(IntField, Negative):
    pass


@export
class NonNegativeInteger(IntField, NonNegative):
    pass


@export
class PositiveInteger(IntField, Positive):
    pass


@export
class SizedString(StringField, Sized):
    pass


@export
class SizedRegexString(SizedString, Regex):
    pass


@export
class PreciseFloat(FloatField):
    def bepsi(self):
        pass


@export
class RegexString(FloatField):
    def bepsi(self):
        pass


@export
class PreciseFloat(FloatField):
    def bepsi(self):
        pass

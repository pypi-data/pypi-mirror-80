#!/usr/bin/env python

## Standard Library
import logging

## TTILS
from .meta import Node
from .validation import *

__all__ = ['A', 'B']

class A(Node):
    _fields = ["parent","child","edges"]
    parent = SizedRegexString("parent", maxlen=20, pattern=r"^[^0-9]")
    child = SizedString("child", maxlen=20)
    edges = NonNegativeInteger("edges")


class B(Node):
    _fields = ["ingress", "egress", "payload"]
    ingress = NonNegativeInteger("ingress")
    egress = NonNegativeInteger("egress")
    payload = SizedRegexString(
        "payload", maxlen=20, pattern=r"[A-Za-z_ ]+$")

"""
Class for a variable that is stored to disk.
Author: Benjamin Dodd (1901386)
"""

import json
import os
from threading import Lock
from atexit import register

from . import LOGGER
from .variable_store import VARIABLE_STORE

class StorableType(object):

    def __init__(self, name: str, default_value = None):
        self.__lock = Lock()
        self.__name = name
        self.__value = default_value

        if self.__name in VARIABLE_STORE:
            self.__value = VARIABLE_STORE[self.__name]
        else:
            VARIABLE_STORE[self.__name] = self.__value



    @property
    def value(self):
        with self.__lock:
            return self.__value

    @value.setter
    def value(self, value):
        with self.__lock:
            self.__value = value
            VARIABLE_STORE[self.__name] = self.__value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"StorableType({self.__name}, {self.__value})"

    def __eq__(self, other):
        return self.value == other

    def __ne__(self, other):
        return self.value != other

    def __lt__(self, other):
        return self.value < other

    def __le__(self, other):
        return self.value <= other

    def __gt__(self, other):
        return self.value > other

    def __ge__(self, other):
        return self.value >= other

    def __add__(self, other):
        return self.value + other

    def __sub__(self, other):
        return self.value - other

    def __mul__(self, other):
        return self.value * other

    def __truediv__(self, other):
        return self.value / other

    def __floordiv__(self, other):
        return self.value // other

    def __mod__(self, other):
        return self.value % other

    def __pow__(self, other):
        return self.value ** other

    def __and__(self, other):
        return self.value & other

    def __or__(self, other):
        return self.value | other

    def __xor__(self, other):
        return self.value ^ other
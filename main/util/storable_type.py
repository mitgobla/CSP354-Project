"""
Class for a variable that is stored to disk.
Author: Benjamin Dodd (1901386)
"""

from threading import Lock

from main.util.variable_store import VariableStore

class StorableType(object):

    def __init__(self, name: str, default_value = None):
        self.store = VariableStore()
        self._lock = Lock()
        self._name = name
        self._value = default_value

        if self._name in self.store:
            self._value = self.store[self._name]
        else:
            self.store[self._name] = self._value



    @property
    def value(self):
        with self._lock:
            return self._value

    @value.setter
    def value(self, value):
        with self._lock:
            self._value = value
            self.store[self._name] = self._value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"StorableType({self._name}, {self._value})"

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
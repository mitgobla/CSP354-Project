"""
Thread-safe singleton class
Author: Benjamin Dodd (1901386)
"""

from threading import Lock

class Singleton(type):
    __instances = {}
    __lock = Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            with cls.__lock:
                if cls not in cls.__instances:
                    cls.__instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.__instances[cls]

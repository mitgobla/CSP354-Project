"""
Thread-safe singleton class
Author: Benjamin Dodd (1901386)
"""

from threading import Lock

class Singleton:
    __instance = None
    __lock = Lock()

    def __new__(cls):
        if cls.__instance is None:
            with cls.__lock:
                if cls.__instance is None:
                    cls.__instance = super(Singleton, cls).__new__(cls)

        return cls.__instance

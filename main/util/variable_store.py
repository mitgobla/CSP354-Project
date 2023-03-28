"""
Class for accessing persistent variable data from disk, and writing new variables to disk
Author: Benjamin Dodd (1910386)
"""

import json
from os import path, makedirs
from threading import Lock

from . import LOGGER

STORE_PATH = path.join("data", "variable_store.json")

class VariableStore:

    def __init__(self):
        self.__lock = Lock()
        self.__data = {}

        if path.exists(STORE_PATH):
            with open(STORE_PATH, "r") as file:
                self.__data = json.load(file)
        else:
            LOGGER.warning("variable_store.json not found, creating new file.")
            if not path.exists(path.dirname(STORE_PATH)):
                makedirs(path.dirname(STORE_PATH))
            with open(STORE_PATH, "w", encoding='utf-8') as file:
                json.dump(self.__data, file)

    def __getitem__(self, key):
        with self.__lock:
            return self.__data[key]

    def __setitem__(self, key, value):
        with self.__lock:
            self.__data[key] = value

            with open(STORE_PATH, "w") as file:
                json.dump(self.__data, file)

    def __contains__(self, key):
        with self.__lock:
            return key in self.__data

    def __delitem__(self, key):
        with self.__lock:
            del self.__data[key]

            with open(STORE_PATH, "w") as file:
                json.dump(self.__data, file)

    def __iter__(self):
        with self.__lock:
            return iter(self.__data)

    def __len__(self):
        with self.__lock:
            return len(self.__data)

VARIABLE_STORE = VariableStore()

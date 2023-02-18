"""
Custom Thread implementation that can be stopped and restarted.
Author: Benjamin Dodd (1901386)
"""

import threading

class WorkerThread(threading.Thread):
    """
    A custom Thread implementation that can be stopped and restarted.
    """

    __id = 0

    def __init__(self, target, *args, **kwargs):
        super().__init__(target = target, args = args, kwargs = kwargs)
        self.__id = WorkerThread.__id
        WorkerThread.__id += 1
        self.__stop_event = threading.Event()

    def __str__(self):
        return f"WorkerThread {self.__id}"

    def __repr__(self) -> str:
        return self.__str__()

    def run(self):
        while not self.__stop_event.is_set():
            super().run()

    def stop(self):
        """
        Stops the thread.
        """
        self.__stop_event.set()

    def restart(self):
        """
        Restarts the thread.
        """
        self.__stop_event.clear()

    def is_stopped(self):
        """
        Returns whether the thread is stopped.
        """
        return self.__stop_event.is_set()

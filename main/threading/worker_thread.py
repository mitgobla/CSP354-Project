"""
Custom Thread implementation that can be stopped and restarted.
Author: Benjamin Dodd (1901386)
"""

import threading

from main.threading import LOGGER
from main.threading.worker_manager import WorkerManager
class WorkerThread(threading.Thread):
    """
    A custom Thread implementation that can be stopped and restarted.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager: WorkerManager = None
        self.__stopped_event = threading.Event()

    def stop(self):
        """
        Stops the thread.
        """
        self.__stopped_event.set()

    def is_stopped(self):
        """
        Returns whether the thread is stopped.

        Returns:
            bool: True if the thread is stopped, False otherwise.
        """
        return self.__stopped_event.is_set()

    def run(self) -> None:
        """
        Runs the thread.
        """
        self.__stopped_event.clear()
        self.work()
        self.manager.remove_worker(self)

    def work(self):
        """
        Override this method to do work in the thread.
        """
        return


if __name__ == "__main__":
    import time

    class MyThread(WorkerThread):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.count = 0

        def work(self):
            while not self.is_stopped():
                print(self.count)
                self.count += 1
                time.sleep(0.5)

    thread = MyThread()
    thread.start()
    time.sleep(5)
    thread.stop()

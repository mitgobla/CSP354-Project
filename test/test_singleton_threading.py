import threading
import unittest

from main.util.singleton import Singleton

class TestSingleton(unittest.TestCase):

    class TestClass(Singleton):
        lock = threading.Lock()
        variable = 5

        def increment_variable(self):
            with self.lock:
                self.variable += 1


    def test_singleton(self):
        self.assertEqual(TestSingleton.TestClass(), TestSingleton.TestClass())

    def test_threading(self):
        # make threads modify the variable
        def modify_variable():
            test_class = TestSingleton.TestClass()
            test_class.increment_variable()


        # create threads
        threads = []
        for _ in range(10):
            threads.append(threading.Thread(target=modify_variable))

        # start threads
        for thread in threads:
            thread.start()

        # wait for threads to finish
        for thread in threads:
            thread.join()

        # check that the variable is the same
        self.assertEqual(TestSingleton.TestClass().variable, 15)

if __name__ == '__main__':
    test = TestSingleton()
    test.test_threading()
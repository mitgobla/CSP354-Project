import unittest

from main.util.storable_type import StorableType

class TestStorableType(unittest.TestCase):

    def test_storable_type(self):
        test = StorableType("test", 0)
        self.assertEqual(test.value, 0)
        test.value = 1
        self.assertEqual(test.value, 1)
        self.assertEqual(test, 1)
        self.assertNotEqual(test, 0)
        self.assertLess(test, 2)
        self.assertLessEqual(test, 2)
        self.assertGreater(test, 0)
        self.assertGreaterEqual(test, 0)
        self.assertEqual(test + 1, 2)
        self.assertEqual(test - 1, 0)
        self.assertEqual(test * 2, 2)
        self.assertEqual(test / 2, 0.5)
        self.assertEqual(test // 2, 0)

    def test_persistence(self):
        test = StorableType("test", 0)
        test.value = 1
        self.assertEqual(test.value, 1)
        test.value = 2
        self.assertEqual(test.value, 2)
        test = StorableType("test", 0)
        self.assertEqual(test.value, 2)
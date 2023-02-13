import unittest

from main.display.circular_display import LeftDisplay, RightDisplay

class TestCircularDisplay(unittest.TestCase):

    def test_singleton(self):
        self.assertEqual(LeftDisplay(), LeftDisplay())
        self.assertEqual(RightDisplay(), RightDisplay())

    def test_not_singleton(self):
        self.assertNotEqual(LeftDisplay(), RightDisplay())
        

if __name__ == '__main__':
    unittest.main()
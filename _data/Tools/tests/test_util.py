from src.util import util

import unittest

class TestUtil(unittest.TestCase):
    def test_capitalise(self):
        self.assertEqual(util.capitalise("hello world"), "Hello World")  # normal
        self.assertEqual(util.capitalise("hello world!"), "Hello World!")  # punctuation
        self.assertEqual(util.capitalise("HELLO WORLD"), "Hello World")  # all caps
        self.assertEqual(util.capitalise("hElLo"), "Hello")  # random, 1 word

    def test_ukCoordsToSectorFile(self):
        self.assertEqual(util.ukCoordsToSectorFile("ABCDEF.GHN", "ABCDEFG.HIW"), ("N0AB.CD.EF.GH0", "WABC.DE.FG.HI0"))  # abstract
        self.assertEqual(util.ukCoordsToSectorFile("503011.88N", "0032833.64W"), ("N050.30.11.880", "W003.28.33.640"))  # random


if __name__ == '__main__':
    unittest.main()

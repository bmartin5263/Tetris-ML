import unittest

from piece import *


class MyTestCase(unittest.TestCase):

    def setUp(self):
        super().setUp()
        random.seed(1442)

    def test_startingPiece_shouldBeInStarters_andNotAllBeTheSame(self):
        pieces = set()
        for i in range(10):
            piece = Pieces.random()
            pieces.add(piece)
            self.assertIn(piece, Pieces.STARTERS)
        self.assertGreater(len(pieces), 2)


if __name__ == '__main__':
    unittest.main()

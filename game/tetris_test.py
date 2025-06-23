import random
import unittest

from game.tetris import *

COLS = 10
ROWS = 24

def emptyRow() -> list[Block]:
    return [Block.Empty for _ in range(COLS)]

def emptyBoard() -> list[list[Block]]:
    return [emptyRow() for _ in range(ROWS)]

def putPiece(board: list[list[Block]], piece: Piece, location: Point) -> list[list[Block]]:
    for point in piece:
        spot = point + location
        board[spot.row][spot.col] = piece.block
    return board

class TetrisTest(unittest.TestCase):

    def setUp(self):
        super().setUp()
        random.seed(1442)
        self.tetris = Tetris(ROWS, COLS)

    def test_create_succeeds(self):
        self.assertIsNotNone(self.tetris)
        self.assertListEqual(putPiece(emptyBoard(), self.tetris.currentPiece, self.tetris.position), self.tetris.board)
        self.assertEqual(self.tetris.STARTING_POINT, self.tetris.position)
        self.assertIn(self.tetris.currentPiece, Pieces.STARTERS)
        self.assertEqual(0, self.tetris.score)

    def test_drop(self):
        self.assertEqual(Pieces.S_0, self.tetris.currentPiece)
        self.assertEqual(Pieces.I_0, self.tetris.nextPiece)
        self.assertEqual(self.tetris.STARTING_POINT, self.tetris.position)
        nextPiece = self.tetris.nextPiece

        self.tetris.makeAction(Action.DROP)

        self.assertEqual(nextPiece, self.tetris.currentPiece)
        self.assertEqual(self.tetris.STARTING_POINT, self.tetris.position)


if __name__ == '__main__':
    unittest.main()

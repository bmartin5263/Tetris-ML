import unittest

from game.tetris import Tetris, Move


class TetrisTest(unittest.TestCase):


    def __init__(self, methodName: str):
        super().__init__(methodName)
        self.tetris = Tetris(rows=10, cols=30)

    def test_create_succeeds(self):
        self.assertIsNotNone(self.tetris)

    def test_makeMove_succeeds(self):
        result = self.tetris.makeMove(Move.MOVE_LEFT)


if __name__ == '__main__':
    unittest.main()

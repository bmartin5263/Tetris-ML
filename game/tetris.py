import config
from piece import *
from typing import Final

@unique
class Move(Enum):
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    MOVE_DOWN = auto()
    ROTATE_CW = auto()
    ROTATE_CCW = auto()
    DROP = auto()

@dataclass(frozen=True)
class Result:
    def __init__(self):
        pass

NO_CHANGE = Result()
OK = Result()
NEXT_PIECE = Result()
GAME_OVER = Result()

class Tetris:
    LEFT = Point(-1, 0)
    RIGHT = Point(1, 0)
    DOWN = Point(0, 1)
    UP = Point(0, -1)

    POINT_VALUES = [100, 300, 1200, 3600]

    def __init__(self):
        self.board: list[list[Block]] = [[Block.Empty for _ in range(config.COLS)] for _ in range(config.ROWS)]
        self.currentPiece: Piece = Pieces.random()
        self.nextPiece: Piece = Pieces.random()
        self.position: Point = Point((config.COLS // 2) - 1, 1)
        self.score: int = 0
        self.rowsCleared: int = 0
        self.combos: list[int] = [0 for _ in range(4)]

    def reset(self):
        self.board: list[list[Block]] = [[Block.Empty for _ in range(config.COLS)] for _ in range(config.ROWS)]
        self._nextPiece()

    def makeMove(self, move: Move) -> Result:
        match move:
            case Move.MOVE_LEFT:
                return self._movePiece(Tetris.LEFT)
            case Move.MOVE_RIGHT:
                return self._movePiece(Tetris.RIGHT)
            case Move.MOVE_DOWN:
                return self._movePiece(Tetris.DOWN)
            case Move.ROTATE_CW:
                return self._rotatePiece(self.currentPiece.cwRotation)
            case Move.ROTATE_CCW:
                return self._rotatePiece(self.currentPiece.ccwRotation)
            case Move.DROP:
                return self._drop()
            case _:
                print('Received invalid move')
                return NO_CHANGE

    def _placePiece(self, piece: Piece, location: Point):
        for point in piece:
            spot = point + location
            assert self.board[spot.row][spot.col] == Block.EMPTY
            self.board[spot.row][spot.col] = piece.block

    def _removePiece(self, piece: Piece, location: Point):
        for point in piece:
            spot = point + location
            assert self.board[spot.row][spot.col] != Block.EMPTY
            self.board[spot.row][spot.col] = Block.EMPTY

    def _canPlacePieceAt(self, piece: Piece, location: Point) -> bool:
        for point in piece:
            spot = point + location
            if spot.row < 0 or spot.row > config.ROWS or spot.col < 0 or spot.col > config.COLS or self.board[spot.row][
                spot.col] != Block.EMPTY:
                return False
        return True

    def _nextPiece(self):
        self.currentPiece = self.nextPiece
        self.nextPiece = Pieces.random()
        self.position: Point = Point((config.COLS // 2) - 1, 1)

    def _movePiece(self, offset: Point) -> Result:
        if offset.x == 0 and offset.y == 0:
            return NO_CHANGE

        isDown = offset.y >= 0
        moved = False

        self._removePiece(self.currentPiece, self.position)
        newPosition = self.position + offset
        if self._canPlacePieceAt(self.currentPiece, newPosition):
            moved = True
            self.position = newPosition
        self._placePiece(self.currentPiece, self.position)

        if isDown and not moved:
            return self._clearRows()
        else:
            return OK

    def _rotatePiece(self, rotation: Piece) -> Result:
        if rotation is self.currentPiece:
            return NO_CHANGE

        didRotate = False

        self._removePiece(self.currentPiece, self.position)
        if self._canPlacePieceAt(rotation, self.position):
            self.currentPiece = rotation
            didRotate = True
        self._placePiece(self.currentPiece, self.position)

        if didRotate:
            return OK
        else:
            return NO_CHANGE

    def _drop(self) -> Result:
        self._removePiece(self.currentPiece, self.position)

        destination = self.position + Tetris.DOWN
        while self._canPlacePieceAt(self.currentPiece, destination):
            destination = destination + Tetris.DOWN
        destination = destination + Tetris.UP

        self._placePiece(self.currentPiece, destination)
        return self._clearRows()

    def _clearRows(self) -> Result:
        rowNumbersToCheck: set[int] = {(point + self.position).row for point in self.currentPiece.body}
        count = len(rowNumbersToCheck)
        if count == 0:
            return NEXT_PIECE

        self.score += Tetris.POINT_VALUES[count - 1]
        self.rowsCleared += count
        self.combos[count - 1] += 1

        for rowNum in rowNumbersToCheck:
            if self._isRowFull(self.board[rowNum]):
                self._clearRow(rowNum)

        return NEXT_PIECE

    def _clearRow(self, rowNumToClear: int):
        while rowNumToClear > 0:
            self.board[rowNumToClear] = self.board[rowNumToClear - 1]
            rowNumToClear -= 1
        Tetris._fillRow(self.board[0], Block.Empty)

    @staticmethod
    def _isRowFull(row: list[Block]):
        for block in row:
            if block == Block.EMPTY:
                return False
        return True

    @staticmethod
    def _fillRow(row: list[Block], block: Block):
        for colNum in range(config.COLS):
            row[colNum] = block

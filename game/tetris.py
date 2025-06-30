from game.piece import *


@unique
class Action(Enum):
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    MOVE_DOWN = auto()
    ROTATE_CW = auto()
    ROTATE_CCW = auto()
    DROP = auto()

@dataclass(frozen=True)
class State:
    board: list[list[Block]]
    currentPiece: Piece
    nextPiece: Piece
    position: Point
    score: int

class Tetris:
    LEFT = Point(-1, 0)
    RIGHT = Point(1, 0)
    DOWN = Point(0, 1)
    UP = Point(0, -1)

    POINT_VALUES = [100, 300, 1200, 3600]

    def __init__(self, rows: int, cols: int):
        self.ROWS = rows
        self.COLS = cols
        self.STARTING_POINT = Point((self.COLS // 2) - 1, 1)


        self.board: list[list[Block]] = [[Block.Empty for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.currentPiece: Piece = Pieces.random()
        self.nextPiece: Piece = Pieces.random()
        self.position: Point = self.STARTING_POINT
        self.score: int = 0
        self.rowsCleared: int = 0
        self.combos: list[int] = [0 for _ in range(4)]
        self.gameOver: bool = False
        self._placePiece(self.currentPiece, self.position)

    def newGame(self):
        self.board: list[list[Block]] = [[Block.Empty for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.gameOver = False
        self.nextPiece: Piece = Pieces.random()
        self.score = 0
        self.rowsCleared = 0
        self.combos = [0 for _ in range(4)]
        self._nextPiece()

    def getState(self):
        return State(self.board, self.currentPiece, self.nextPiece, self.position, self.score)

    def _placePiece(self, piece: Piece, location: Point):
        for point in piece:
            spot = point + location
            assert self.board[spot.row][spot.col] == Block.Empty
            self.board[spot.row][spot.col] = piece.block

    def _removePiece(self, piece: Piece, location: Point):
        for point in piece:
            spot = point + location
            assert self.board[spot.row][spot.col] != Block.Empty
            self.board[spot.row][spot.col] = Block.Empty

    def _canPlacePieceAt(self, piece: Piece, location: Point) -> bool:
        for point in piece:
            spot = point + location
            if spot.row < 0 or spot.row >= self.ROWS or spot.col < 0 or spot.col >= self.COLS or self.board[spot.row][spot.col] != Block.Empty:
                return False
        return True

    #   if (!canPlacePiece(currentPiece, currentPosition)) {
    #     currentPosition.y -= 1;
    #     if (!canPlacePiece(currentPiece, currentPosition)) {
    #       for (auto& row : board) {
    #         for (auto& c : row) {
    #           if (c != Color::OFF()) {
    #             c = Color(.03f, .03f, .03f);
    #           }
    #         }
    #       }
    #       gameOver = true;
    #     }
    #   }

    def _nextPiece(self):
        print("Next Piece")
        self.currentPiece = self.nextPiece
        self.nextPiece = Pieces.random()
        self.position: Point = self.STARTING_POINT

        if not self._canPlacePieceAt(self.currentPiece, self.position):
            self.position = self.position + Tetris.UP
            if not self._canPlacePieceAt(self.currentPiece, self.position):
                self.gameOver = True
                for point in self.currentPiece:
                    spot = point + self.position
                    self.board[spot.row][spot.col] = self.currentPiece.block
                return

        self._placePiece(self.currentPiece, self.position)

    def movePiece(self, offset: Point):
        if (offset.x == 0 and offset.y == 0) or self.gameOver:
            return

        isDown = offset.y > 0
        moved = False

        self._removePiece(self.currentPiece, self.position)
        newPosition = self.position + offset
        if self._canPlacePieceAt(self.currentPiece, newPosition):
            moved = True
            self.position = newPosition
        self._placePiece(self.currentPiece, self.position)

        if isDown and not moved:
            self._clearRows()

    def rotateClockwise(self):
        self._rotatePiece(self.currentPiece.cwRotation)

    def rotateCounterClockwise(self):
        self._rotatePiece(self.currentPiece.ccwRotation)

    def _rotatePiece(self, rotation: Piece):
        if rotation is self.currentPiece or self.gameOver:
            return

        self._removePiece(self.currentPiece, self.position)
        if self._canPlacePieceAt(rotation, self.position):
            self.currentPiece = rotation
        self._placePiece(self.currentPiece, self.position)

    def drop(self):
        if self.gameOver:
            return
        self._removePiece(self.currentPiece, self.position)

        destination = self.position + Tetris.DOWN
        while self._canPlacePieceAt(self.currentPiece, destination):
            destination = destination + Tetris.DOWN
        destination = destination + Tetris.UP

        self._placePiece(self.currentPiece, destination)
        self.position = destination
        self._clearRows()

    def _clearRows(self):
        rowNumbersToCheck: set[int] = {(point + self.position).row for point in self.currentPiece.body}
        print("Row numbers to check:", sorted(rowNumbersToCheck))

        numberOfClearedRows = 0
        for rowNum in sorted(rowNumbersToCheck):
            if self._isRowFull(self.board[rowNum]):
                self._clearRow(rowNum)
                numberOfClearedRows += 1

        if numberOfClearedRows > 0:
            print("Cleared {} row(s). Earning {} points".format(numberOfClearedRows,
                                                                Tetris.POINT_VALUES[numberOfClearedRows - 1]))
            self.score += Tetris.POINT_VALUES[numberOfClearedRows - 1]
            self.rowsCleared += numberOfClearedRows
            self.combos[numberOfClearedRows - 1] += 1

        self._nextPiece()

    def _clearRow(self, rowNumToClear: int):
        while rowNumToClear > 0:
            Tetris._copyRow(self.board[rowNumToClear], self.board[rowNumToClear - 1])
            rowNumToClear -= 1
        Tetris._fillRow(self.board[0], Block.Empty)

    @staticmethod
    def _isRowFull(row: list[Block]):
        for block in row:
            if block == Block.Empty:
                return False
        return True

    @staticmethod
    def _fillRow(row: list[Block], block: Block):
        for colNum in range(len(row)):
            row[colNum] = block

    @staticmethod
    def _copyRow(dst: list[Block], src: list[Block]):
        for colNum in range(len(dst)):
            dst[colNum] = src[colNum]

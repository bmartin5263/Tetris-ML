import random
from dataclasses import dataclass
from typing import NamedTuple, Optional
from enum import Enum, unique, auto

@dataclass(frozen=True)
class Point:
    x: int
    y: int

    @property
    def col(self) -> int:
        return self.x

    @property
    def row(self) -> int:
        return self.y

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y)

    def __neg__(self) -> "Point":
        return Point(-self.x, -self.y)

    def __mul__(self, scalar: int) -> "Point":
        return Point(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: int) -> "Point":
        return self * scalar


@unique
class Block(Enum):
    L = auto()
    J = auto()
    Z = auto()
    S = auto()
    T = auto()
    O = auto()
    I = auto()
    Empty = auto()

class Piece:

    def __init__(self, block: Block, body: list[Point]):
        self.block = block
        self.body = body
        self.ccwRotation: Piece | None = None
        self.cwRotation: Piece | None = None

    def __iter__(self):
        return iter(self.body)

    def setRotations(self, ccwRotation: "Piece", cwRotation: "Piece"):
        self.ccwRotation = ccwRotation
        self.cwRotation = cwRotation


class Pieces:
    O_0 = Piece(Block.O, [Point(0, 0), Point(1, 0), Point(0, 1), Point(1, 1)])
    J_0 = Piece(Block.J, [Point(0, 0), Point(1, 0), Point(2, 0), Point(2, 1)])
    J_1 = Piece(Block.J, [Point(1, -1), Point(1, 0), Point(0, 1), Point(1, 1)])
    J_2 = Piece(Block.J, [Point(0, 0), Point(0, 1), Point(1, 1), Point(2, 1)])
    J_3 = Piece(Block.J, [Point(0, -1), Point(1, -1), Point(0, 0), Point(0, 1)])
    L_0 = Piece(Block.L, [Point(0, 0), Point(1, 0), Point(2, 0), Point(0, 1)])
    L_1 = Piece(Block.L, [Point(0, -1), Point(1, -1), Point(1, 0), Point(1, 1)])
    L_2 = Piece(Block.L, [Point(2, 0), Point(0, 1), Point(1, 1), Point(2, 1)])
    L_3 = Piece(Block.L, [Point(0, -1), Point(0, 0), Point(0, 1), Point(1, 1)])
    T_0 = Piece(Block.T, [Point(0, 0), Point(1, 0), Point(2, 0), Point(1, 1)])
    T_1 = Piece(Block.T, [Point(2, -1), Point(1, 0), Point(2, 0), Point(2, 1)])
    T_2 = Piece(Block.T, [Point(1, 0), Point(0, 1), Point(1, 1), Point(2, 1)])
    T_3 = Piece(Block.T, [Point(0, -1), Point(1, 0), Point(0, 0), Point(0, 1)])
    Z_0 = Piece(Block.Z, [Point(0, 0), Point(1, 0), Point(1, 1), Point(2, 1)])
    Z_1 = Piece(Block.Z, [Point(1, -1), Point(1, 0), Point(0, 0), Point(0, 1)])
    S_0 = Piece(Block.S, [Point(1, 0), Point(2, 0), Point(0, 1), Point(1, 1)])
    S_1 = Piece(Block.S, [Point(0, -1), Point(0, 0), Point(1, 0), Point(1, 1)])
    I_0 = Piece(Block.I, [Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0)])
    I_1 = Piece(Block.I, [Point(2, -1), Point(2, 0), Point(2, 1), Point(2, 2)])

    O_0.setRotations(O_0, O_0)
    J_0.setRotations(J_3, J_1)
    J_1.setRotations(J_0, J_2)
    J_2.setRotations(J_1, J_3)
    J_3.setRotations(J_2, J_0)
    L_0.setRotations(L_3, L_1)
    L_1.setRotations(L_0, L_2)
    L_2.setRotations(L_1, L_3)
    L_3.setRotations(L_2, L_0)
    T_0.setRotations(T_3, T_1)
    T_1.setRotations(T_0, T_2)
    T_2.setRotations(T_1, T_3)
    T_3.setRotations(T_2, T_0)
    Z_0.setRotations(Z_1, Z_1)
    Z_1.setRotations(Z_0, Z_0)
    S_0.setRotations(S_1, S_1)
    S_1.setRotations(S_0, S_0)
    I_0.setRotations(I_1, I_1)
    I_1.setRotations(I_0, I_0)

    ALL = [O_0, J_0, J_1, J_2, J_3, L_0, L_1, L_2, L_3, T_0, T_1, T_2, T_3, Z_0, Z_1, S_0, S_1, I_0, I_1]
    STARTERS = [O_0, J_0, L_0, T_0, Z_0, S_0, I_0]

    @staticmethod
    def random() -> Piece:
        return random.choice(Pieces.ALL)

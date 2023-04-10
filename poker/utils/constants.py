from enum import Enum


SUITS = ["hearts", "diamonds", "spades", "clubs"]
FACE_CARDS = "J Q K A".split()
NUMBER_CARDS = list(range(2, 11))
INCREMENT_LIMIT = 100
SINGLE_CHIP = 1
DOUBLE = 2
COMPETITION = (list(range(1, 4)))


class Chip(Enum):
    WHITE = 1
    RED = 5
    BLUE = 10


class Cash(Enum):
    FIVE = 5
    TEN = 10
    FIFTEEN = 15
    TWENTY = 20
    FIFTY = 50
    HUNDRED = 100


class Blind(Enum):
    SMALL = 1
    BIG = 2


class Decision(Enum):
    YES = "yes"
    NO = "no"
    Y = "y"
    N = "n"
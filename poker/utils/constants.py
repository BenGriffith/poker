from enum import Enum

import emoji

SUITS = f"{emoji.emojize(':heart_suit:')} {emoji.emojize(':diamond_suit:')} {emoji.emojize(':spade_suit:')} {emoji.emojize(':club_suit:')}".split()
NUMBER_CARDS = list(range(2, 11))
INCREMENT_LIMIT = 100
SINGLE_CHIP = 1
DOUBLE = 2
COMPETITION = list(range(1, 5))
PLAYER_NAME = "You"
GAME_DELAY = 2
PLAYER_TABLE_COLUMNS = "Order, Name, Chips, Blind, Pocket Cards, Best Hand, Short Name".split(",")
FIRST_PLAYER = 1
HIDDEN = "Hidden"
TIE = 3

class BetAction(Enum):
    CHECK = "check"
    RAISE = "raise"
    CALL = "call"
    FOLD = "fold"


class BetValue(Enum):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    TEN = 10


class PlayerKind(Enum):
    PLAYER = "Player"
    COMPUTER = "Computer"


class FaceCards(Enum):
    J = 11
    Q = 12
    K = 13
    A = 14


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
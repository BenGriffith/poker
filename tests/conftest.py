import pytest

from poker.utils.card import Card
from poker.utils.deck import Deck
from poker.utils.chip import PlayerStack, GameStack
from poker.utils.constants import Chip, Cash


@pytest.fixture
def card():
    return Card("hearts", "10")

@pytest.fixture
def deck():
    return Deck()

@pytest.fixture
def player_stack():
    return PlayerStack()

@pytest.fixture
def game_stack():
    return GameStack()

@pytest.fixture
def chip():
    return Chip

@pytest.fixture
def cash():
    return Cash
import pytest

from poker.utils.card import Card
from poker.utils.deck import Deck
from poker.utils.chip import PlayerStack, GameStack
from poker.utils.constants import Cash


@pytest.fixture
def card_number():
    return Card("hearts", "10")

@pytest.fixture
def card_face():
    return Card("hearts", "K")

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
def cash():
    return Cash

@pytest.fixture
def thirty_chips(player_stack, cash):
    player_stack.increment(cash.FIVE.value)
    player_stack.increment(cash.FIVE.value)
    player_stack.increment(cash.TWENTY.value)

@pytest.fixture
def fifty_chips(player_stack, cash):
    player_stack.increment(cash.TEN.value)
    player_stack.increment(cash.FIFTEEN.value)
    player_stack.increment(cash.TWENTY.value)
    player_stack.increment(cash.FIVE.value)
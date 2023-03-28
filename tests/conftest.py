import pytest

from poker.utils.card import Card
from poker.utils.deck import Deck
from poker.utils.chip import Stack
from poker.utils.constants import Chip, Cash


@pytest.fixture
def card():
    return Card("hearts", "10")

@pytest.fixture
def deck():
    return Deck()

@pytest.fixture
def stack():
    return Stack()

@pytest.fixture
def chip():
    return Chip

@pytest.fixture
def cash():
    return Cash
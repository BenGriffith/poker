import pytest

from poker.utils.card import Card
from poker.utils.deck import Deck
from poker.utils.constants import SUITS, FACE_CARDS, NUMBER_CARDS


@pytest.fixture
def card():
    return Card("hearts", "10")

@pytest.fixture
def deck():
    return Deck()
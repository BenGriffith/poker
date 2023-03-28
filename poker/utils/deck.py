from random import shuffle

from poker.utils.card import Card
from poker.utils.constants import SUITS, FACE_CARDS, NUMBER_CARDS


class Deck:

    def __init__(self) -> None:
        self.cards: list[Card] = []
        self._create_deck()

    def _create_deck(self):
        _cards = NUMBER_CARDS + FACE_CARDS
        for suit in SUITS:
            _suits = [suit for _ in range(len(_cards))]
            for _suit, _card in zip(_suits, _cards):
                self.cards.append(Card(_suit, _card))

    def shuffle_deck(self):
        shuffle(self.cards)
from typing import List
from random import shuffle

from utils.card import Card
from utils.setup import SUITS, FACE_CARDS, NUMBER_CARDS


class Deck:

    def __init__(self) -> None:
        self.cards: List[Card] = []
        self._create_deck()

    def _create_deck(self):
        _cards = NUMBER_CARDS + FACE_CARDS
        for suit in SUITS:
            for _suit, _card in zip([suit for _ in range(len(_cards))], _cards):
                self.cards.append(Card(_suit, _card))

    def shuffle_deck(self):
        shuffle(self.cards)
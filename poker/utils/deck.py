from poker.utils.card import Card
from poker.utils.constants import SUITS, NUMBER_CARDS, FaceCards


class Deck:

    def __init__(self) -> None:
        self.cards: list[Card] = []
        self._create_deck()

    def _create_deck(self):
        """
        Create deck of cards
        """
        _cards = NUMBER_CARDS + [item.name for item in FaceCards]
        for suit in SUITS:
            _suits = [suit for _ in range(len(_cards))]
            for _suit, _card in zip(_suits, _cards):
                self.cards.append(Card(suit=_suit, rank=_card))
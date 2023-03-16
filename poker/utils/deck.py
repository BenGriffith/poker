from typing import List

from utils.card import Card
from utils.setup import SUITS, FACE_CARDS, NUMBER_CARDS


class Deck:

    def __init__(self):
        self.cards = List[Card]


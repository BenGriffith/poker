from random import shuffle

from poker.utils.chip import PlayerStack
from poker.utils.deck import Deck, Card


class Player:

    def __init__(self, name: str = None, cash: int = 0) -> None:
        self.name = name
        self.cash = cash
        self.hand: list[Card] = []
        self.stack = PlayerStack()

    def buy_chips(self, value: int) -> None:
        self.stack.increment(value)
        self.cash -= value


class Computer(Player):

    def __init__(self, name, cash) -> None:
        Player.__init__(self, name, cash)


class Dealer(Player):

    def __init__(self) -> None:
        self.deck = Deck()
        self.hand: list[Card] = []

    def shuffle_deck(self) -> None:
        shuffle(self.deck.cards)

    def deal_card(self, person: any) -> None:
        card = self.deck.cards.pop()
        person.hand.append(card)
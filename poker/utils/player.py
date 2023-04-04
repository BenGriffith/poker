from random import shuffle

from poker.utils.chip import PlayerStack
from poker.utils.deck import Deck


class Player:

    def __init__(self, cash: int) -> None:
        self.cash = cash
        self.hand = []
        self.chips = PlayerStack

    def buy_chips(self, value: int) -> None:
        self.chips.increment(value)
        self.cash -= value


class Computer(Player):

    def __init__(self) -> None:
        Player.__init__(self)


class Dealer(Player):

    def __init__(self) -> None:
        self.deck = Deck()

    def shuffle_deck(self) -> None:
        shuffle(self.deck.cards)

    def deal_card(self, player: Player) -> None:
        card = self.deck.cards.pop()
        player.hand.append(card)
import random

from poker.utils.chip import PlayerStack
from poker.utils.deck import Deck, Card
from poker.utils.constants import Chip


class Player:

    def __init__(self, name: str = None, cash: int = 0) -> None:
        self.name = name
        self.cash = cash
        self.hand: list[Card] = []
        self.stack = PlayerStack()
        self.kind = self.__class__.__name__

    def buy_chips(self, value: int) -> None:
        self.stack.increment(value)
        self.cash -= value

    def process_action(self, raise_amount: int) -> int:
        if raise_amount == 0:
            # bet
            self.stack.decrement(Chip.WHITE.name, raise_amount)
            return raise_amount
        else: 
            # match bet or call
            self.stack.decrement(Chip.WHITE.name, raise_amount)
            return raise_amount


class Computer(Player):

    def __init__(self, name, cash) -> None:
        Player.__init__(self, name, cash)

    def select_action(self, raise_amount: int) -> str:
        if raise_amount == 0:
            return random.choice(["check", "raise"])
        else:
            if raise_amount <= self.stack.cash_equivalent():
                return "call"
            else:
                return "fold"
                

    def process_action(self, raise_amount: int) -> int:
        white, red, blue = self.stack.chip_count()
        if raise_amount == 0:
            # random bet or bet
            white_third = white // 3
            white_chips = random.randint(1, white_third)
            self.stack.decrement(Chip.WHITE.name, white_chips)
            return white_chips
        else: 
            # match bet or call
            self.stack.decrement(Chip.WHITE.name, raise_amount)
            return raise_amount
            

class Dealer(Player):

    def __init__(self) -> None:
        self.deck = Deck()
        self.hand: list[Card] = []

    def shuffle_deck(self) -> None:
        random.shuffle(self.deck.cards)

    def deal_card(self, person: any) -> None:
        card = self.deck.cards.pop()
        person.hand.append(card)
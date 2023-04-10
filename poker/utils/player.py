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

    def process_action(self, increase: int) -> int:
        if increase == 0:
            # bet
            self.stack.decrement(Chip.WHITE.name, increase)
            return increase
        else: 
            # match bet or call
            self.stack.decrement(Chip.WHITE.name, increase)
            return increase


class Computer(Player):

    def __init__(self, name, cash) -> None:
        Player.__init__(self, name, cash)

    def select_action(self, increase: int) -> str:
        if increase == 0:
            return random.choice(["check", "increase"])
        else:
            if increase <= self.stack.cash_equivalent():
                return "call"
            else:
                return "fold"
                

    def process_action(self, increase: int) -> int:
        white, red, blue = self.stack.chip_count()
        if increase == 0:
            # random bet or bet
            white_third = white // 3
            white_chips = random.randint(1, white_third)
            self.stack.decrement(Chip.WHITE.name, white_chips)
            return white_chips
        else: 
            # match bet or call
            self.stack.decrement(Chip.WHITE.name, increase)
            return increase
            

class Dealer(Player):

    def __init__(self) -> None:
        self.deck = Deck()
        self.hand: list[Card] = []

    def shuffle_deck(self) -> None:
        random.shuffle(self.deck.cards)

    def deal_card(self, person: any) -> None:
        card = self.deck.cards.pop()
        person.hand.append(card)
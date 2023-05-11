import random

from poker.utils.chip import PlayerStack
from poker.utils.deck import Deck, Card
from poker.utils.constants import BetAction, BetValue, PlayerKind


class Player:

    def __init__(self, name: str = None, cash: int = 0) -> None:
        self.name = name
        self.cash = cash
        self.pocket_cards: list[Card] = []
        self.stack = PlayerStack()
        self.kind = self.__class__.__name__
        self.best_hand = {}

    def buy_chips(self, value: int) -> None:
        """
        Increment player chip count
        """
        self.stack.increment(cash=value)
        self.cash -= value

    def process_bet(self, raise_amount: int) -> int:
        """
        Decrement player chip count
        """
        self.stack.decrement(chip=self.stack.white.get("name"), value=raise_amount)
        return raise_amount


class Computer(Player):

    def __init__(self, name, cash) -> None:
        Player.__init__(self, name, cash)

    def select_action(self, raise_amount: int) -> str:
        """
        Based off raise amount, select computer action
        """
        if raise_amount == BetValue.ZERO.value:
            if self.stack.chips["White"] == BetValue.ZERO.value:
                return BetAction.CHECK.value
            else:
                return random.choice([BetAction.CHECK.value, BetAction.RAISE.value])
        else:
            if raise_amount <= self.stack.chips["White"]:
                return BetAction.CALL.value
            else:
                return BetAction.FOLD.value            

    def process_bet(self, raise_amount: int) -> int:
        """
        Process computer bet by calculating a random amount or calling a raise
        """
        if raise_amount == BetValue.ZERO.value:
            # random bet or bet
            if self.stack.chips["White"] == BetValue.ONE.value:
                white_chips = self.stack.chips["White"]
            elif self.stack.chips["White"] <= BetValue.TEN.value:
                white_chips = random.choice(list(range(1, self.stack.chips["White"] + 1)))
            else:
                white_third = self.stack.chips["White"] // BetValue.THREE.value
                white_chips = random.randint(1, white_third)
            self.stack.decrement(chip=self.stack.white.get("name"), value=white_chips)
            return white_chips
        else: 
            # match bet or call
            self.stack.decrement(chip=self.stack.white.get("name"), value=raise_amount)
            return raise_amount
            

class Dealer(Player):

    def __init__(self) -> None:
        self.deck = Deck()
        self.hand: list[Card] = []
        self.kind = self.__class__.__name__

    def shuffle_deck(self) -> None:
        random.shuffle(self.deck.cards)

    def deal_card(self, person: any) -> None:
        """
        Deal card for player and dealer/community cards
        """
        card = self.deck.cards.pop()
        if person.kind in [PlayerKind.PLAYER.value, PlayerKind.COMPUTER.value]:
            person.pocket_cards.append(card)
        else:
            person.hand.append(card)
from poker.utils.chip import GameStack
from poker.utils.player import Player


class Action:

    def __init__(self, game_stack: GameStack, player: Player) -> None:
        self.game_stack = game_stack
        self.person = player

    def check(self) -> None:
        pass

    def bet(self, chip: str, value: int) -> None:
        self.game_stack.increment(chip, value)
        self.person.stack.decrement(chip, value)

    def call(self, chip: str, value: int) -> None:
        self.bet(chip, value)

    def fold(self) -> None:
        self.person.hand = []

    def increase(self, chip: str, value: int) -> None: # raise
        self.bet(chip, value)

    def blind(self, chip: str, value: int) -> None:
        self.bet(chip, value)
from poker.utils.chip import GameStack


class Action:

    def __init__(self, game_stack: GameStack, player: any = None) -> None:
        self.game_stack = game_stack
        self.person = player

    def bet(self, chip: str, value: int) -> None:
        self.game_stack.increment(chip=chip, quantity=value)
        self.person.stack.decrement(chip=chip, value=value)

    def call(self, chip: str, value: int) -> None:
        self.bet(chip=chip, value=value)

    def fold(self) -> None:
        self.person.pocket_cards = []

    def increase(self, chip: str, value: int) -> None: # raise
        self.bet(chip=chip, value=value)

    def blind(self, chip: str, value: int) -> None:
        self.bet(chip=chip, value=value)
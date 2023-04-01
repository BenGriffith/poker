from poker.utils.chip import PlayerStack


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
        self.hand = []        
class Card:

    def __init__(self, suit, rank) -> None:
        self.suit = suit
        self.rank = rank

    def value(self):
        pass

    def __str__(self) -> str:
        return f"{self.suit}, {self.rank}"
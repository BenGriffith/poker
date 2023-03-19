class Card:

    def __init__(self, suit: str, rank: str) -> None:
        self.suit = suit
        self.rank = rank

    def value(self):
        pass

    def __str__(self) -> str:
        return f"{self.suit}, {self.rank}"
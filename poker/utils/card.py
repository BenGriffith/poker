from poker.utils.constants import FaceCards


class Card:

    def __init__(self, suit: str, rank: str) -> None:
        self.suit = suit
        self.rank = rank

    def value(self) -> int:
        """
        Provide numeric value for face cards
        """
        return FaceCards[self.rank].value

    def __str__(self) -> str:
        return f"({self.suit}, {self.rank})"
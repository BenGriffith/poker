from collections import defaultdict

from poker.utils.constants import INCREMENT_LIMIT, SINGLE_CHIP, DOUBLE, Chip, Cash
from poker.utils.exception import IncrementException, CashException


class Stack:

    def __init__(self) -> None:
        self.chips = defaultdict(int)
    
    # increment chips
    def increment(self, cash: int) -> None:
        if cash > INCREMENT_LIMIT:
            raise IncrementException()
        
        chip_values = [item.value for item in Cash]
        if cash not in chip_values:
            raise CashException()
        
        if cash == Cash.FIVE.value:
            self.chips[Chip.WHITE.name] += SINGLE_CHIP * Cash.FIVE.value
        elif cash == Cash.TEN.value:
            self.chips[Chip.WHITE.name] += SINGLE_CHIP * Cash.FIVE.value
            self.chips[Chip.RED.name] += SINGLE_CHIP
        elif cash == Cash.FIFTEEN.value:
            self.chips[Chip.RED.name] += SINGLE_CHIP
            self.chips[Chip.BLUE.name] += SINGLE_CHIP
        else:
            self.chips[Chip.RED.name] += SINGLE_CHIP * DOUBLE
            self.chips[Chip.BLUE.name] += SINGLE_CHIP
    
    # decrement chips
    def decrement(self, chip: str, value: int) -> None:
        self.chips[chip] -= value

    # redeem
    def redeem(self):
        pass

    # count
    def chip_count(self) -> tuple:
        return (
            self.chips[Chip.WHITE.name],
            self.chips[Chip.RED.name],
            self.chips[Chip.BLUE.name],
            )

    # cash
    def cash_equivalent(self):
        WHITE = self.chips[Chip.WHITE.name] * Chip.WHITE.value
        RED = self.chips[Chip.RED.name] * Chip.RED.value
        BLUE = self.chips[Chip.BLUE.name] * Chip.BLUE.value
        return WHITE + RED + BLUE
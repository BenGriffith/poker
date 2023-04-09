from collections import Counter

from poker.utils.constants import INCREMENT_LIMIT, SINGLE_CHIP, DOUBLE, Chip, Cash
from poker.utils.exception import IncrementException, CashException


class PlayerStack:

    def __init__(self) -> None:
        self.chips = Counter()
    
    def increment(self, cash: int) -> None:
        if cash > INCREMENT_LIMIT:
            raise IncrementException()
        
        chip_values = [item.value for item in Cash]
        if cash not in chip_values:
            raise CashException()
        
        if cash == Cash.FIVE.value:
            self.chips[Chip.WHITE.name] += SINGLE_CHIP * Cash.FIVE.value
        elif cash == Cash.TEN.value:
            self.chips[Chip.WHITE.name] += SINGLE_CHIP * Cash.TEN.value
        elif cash == Cash.FIFTEEN.value:
            self.chips[Chip.WHITE.name] += SINGLE_CHIP * Cash.FIFTEEN.value
        else:
            self.chips[Chip.WHITE.name] += SINGLE_CHIP * Cash.TWENTY.value

    
    def decrement(self, chip: str, value: int) -> None:
        self.chips[chip] -= value

    def redeem(self):
        """
        Exchange higher value chips for lower value chips
        """
        pass

    def chip_count(self) -> tuple:
        return (
            self.chips[Chip.WHITE.name],
            self.chips[Chip.RED.name],
            self.chips[Chip.BLUE.name],
            )


    def cash_equivalent(self):
        white = self.chips[Chip.WHITE.name] * Chip.WHITE.value
        red = self.chips[Chip.RED.name] * Chip.RED.value
        blue = self.chips[Chip.BLUE.name] * Chip.BLUE.value
        return white + red + blue
    

class GameStack(PlayerStack):

    def __init__(self) -> None:
        PlayerStack.__init__(self)

    def increment(self, chip: str, quantity: int) -> None:
        self.chips[chip] += quantity        

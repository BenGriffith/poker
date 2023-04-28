from collections import Counter

from poker.utils.constants import INCREMENT_LIMIT, SINGLE_CHIP, Cash
from poker.utils.exception import IncrementException, CashException


class PlayerStack:

    WHITE = {"name": "White", "value": 1}
    BLUE = {"name": "Blue", "value": 5}
    RED = {"name": "Red", "value": 10}

    def __init__(self) -> None:
        self.chips = Counter()
    
    def increment(self, cash: int) -> None:
        if cash > INCREMENT_LIMIT:
            raise IncrementException
        
        chip_values = [item.value for item in Cash]
        if cash not in chip_values:
            raise CashException
        
        if cash == Cash.FIVE.value:
            self.chips[self.WHITE["name"]] += SINGLE_CHIP * Cash.FIVE.value
        elif cash == Cash.TEN.value:
            self.chips[self.WHITE["name"]] += SINGLE_CHIP * Cash.TEN.value
        elif cash == Cash.FIFTEEN.value:
            self.chips[self.WHITE["name"]] += SINGLE_CHIP * Cash.FIFTEEN.value
        elif cash == Cash.TWENTY.value:
            self.chips[self.WHITE["name"]] += SINGLE_CHIP * Cash.TWENTY.value
        elif cash == Cash.FIFTY.value:
            self.chips[self.WHITE["name"]] += SINGLE_CHIP * Cash.FIFTY.value
        else:
            self.chips[self.WHITE["name"]] += SINGLE_CHIP * Cash.HUNDRED.value
    
    def decrement(self, chip: str, value: int) -> None:
        self.chips[chip] -= value
    
    def chip_count(self) -> tuple:
        return (
            self.chips[self.WHITE["name"]],
            self.chips[self.RED["name"]],
            self.chips[self.BLUE["name"]],
            )

    def cash_equivalent(self):
        white = self.chips[self.WHITE["name"]] * self.WHITE["value"]
        red = self.chips[self.RED["name"]] * self.RED["value"]
        blue = self.chips[self.BLUE["name"]] * self.BLUE["value"]
        return white + red + blue
    

class GameStack(PlayerStack):

    def __init__(self) -> None:
        PlayerStack.__init__(self)

    def increment(self, chip: str, quantity: int) -> None:
        self.chips[chip] += quantity        

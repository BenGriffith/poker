from collections import Counter

from poker.utils.constants import INCREMENT_LIMIT, SINGLE_CHIP, Cash
from poker.utils.exception import IncrementException, CashException


class PlayerStack:

    white = {"name": "White", "value": 1}
    red = {"name": "Red", "value": 5}
    blue = {"name": "Blue", "value": 10}

    def __init__(self) -> None:
        self.chips = Counter()
    
    def increment(self, cash: int) -> None:
        """
        Increment player chip count
        """
        if cash > INCREMENT_LIMIT:
            raise IncrementException
        
        chip_values = [item.value for item in Cash]
        if cash not in chip_values:
            raise CashException
        
        if cash == Cash.FIVE.value:
            self.chips[self.white["name"]] += SINGLE_CHIP * Cash.FIVE.value
        elif cash == Cash.TEN.value:
            self.chips[self.white["name"]] += SINGLE_CHIP * Cash.TEN.value
        elif cash == Cash.FIFTEEN.value:
            self.chips[self.white["name"]] += SINGLE_CHIP * Cash.FIFTEEN.value
        elif cash == Cash.TWENTY.value:
            self.chips[self.white["name"]] += SINGLE_CHIP * Cash.TWENTY.value
        elif cash == Cash.FIFTY.value:
            self.chips[self.white["name"]] += SINGLE_CHIP * Cash.FIFTY.value
        else:
            self.chips[self.white["name"]] += SINGLE_CHIP * Cash.HUNDRED.value
    
    def decrement(self, chip: str, value: int) -> None:
        """
        Decrement player chip count
        """
        self.chips[chip] -= value

    def cash_equivalent(self):
        """
        Convert chips to cash
        """
        white = self.chips[self.white["name"]] * self.white["value"]
        red = self.chips[self.red["name"]] * self.red["value"]
        blue = self.chips[self.blue["name"]] * self.blue["value"]
        return white + red + blue
    

class GameStack(PlayerStack):

    def increment(self, chip: str, quantity: int) -> None:
        self.chips[chip] += quantity   
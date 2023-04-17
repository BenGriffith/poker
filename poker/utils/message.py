from poker.utils.constants import Blind, Decision, Cash, COMPETITION, Chip
from poker.utils.exception import NegativeException, RangeException, CashException


class GameMessage:

    def __init__(self) -> None:
        self.cash_options = [item.value for item in Cash]
        self.decision = [item.value for item in Decision]


    def play(self) -> bool:
        player_response = input("Welcome to Texas hold'em! Would you like to play a game? [yes/no] ").lower()
        if player_response in [Decision.Y.value, Decision.YES.value]:
            return True
        return False

    
    def ask_name(self) -> str:
        player_response = input("What is your name? ").strip().capitalize()
        if player_response == "":
            return "Tron"
        return player_response
    
    
    def starting_cash(self, name: str) -> int:
        player_response = int(input(f"{name}, how much money would you like to start off with? {self.cash_options} "))
        if player_response not in self.cash_options:
            raise CashException
        return player_response
    
    
    def competition(self, name: str) -> int:
        competition_num = int(input(f"{name}, how many players would you like to play against? [1 to 3] "))
        if competition_num not in COMPETITION:
            raise RangeException
        competition_cash = int(input(f"How much cash should each player get? {self.cash_options} "))
        if competition_cash not in self.cash_options:
            raise CashException
        return competition_num, competition_cash
    
    
    def action(self, name: str, has_raise: bool, raise_amount: int) -> str:
        if has_raise:
            player_response = input(f"{name}, another player raised the bet by {raise_amount}, what would you like to do? ") # call or fold
        else:
            player_response = input(f"{name}, what would you like to do? ")
        return player_response
    
    
    def increase(self, name: str) -> int:
        player_response = int(input(f"{name}, how much would you like to raise? "))
        return player_response
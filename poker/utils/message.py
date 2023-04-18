from rich.table import Table

from poker.utils.constants import Blind, Decision, Cash, COMPETITION, Chip
from poker.utils.exception import NegativeException, RangeException, CashException
from poker.utils.chip import GameStack


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
    
    
    def competition_count(self, name: str) -> int:
        count = int(input(f"{name}, how many players would you like to play against? {COMPETITION} "))
        if count not in COMPETITION:
            raise RangeException
        return count


    def competition_cash(self, name: str) -> int:
        cash = int(input(f"{name}, how much cash should each player get? {self.cash_options} "))
        if cash not in self.cash_options:
            raise CashException
        return cash
    
    
    def action(self, name: str, has_raise: bool, raise_amount: int) -> str:
        if has_raise:
            player_response = input(f"{name}, another player raised the bet by {raise_amount}, what would you like to do? ") # call or fold
        else:
            player_response = input(f"{name}, what would you like to do? ")
        return player_response
    
    
    def increase(self, name: str) -> int:
        player_response = int(input(f"{name}, how much would you like to raise? "))
        return player_response
    

    def summary(self, pot: GameStack, community_cards: list, players: dict) -> tuple:

        game_pot_table = Table(title="Pot")
        game_pot_table.add_column("Chip")
        game_pot_table.add_column("Chip Count")
        game_pot_table.add_row("1", "2")

        game_cards_table = Table(title="Community Cards")
        game_cards_table.add_column("Cards")
        game_cards_table.add_row("test")

        player_table = Table(title="Player Summary")
        player_table.add_column("Player Order")
        player_table.add_column("Player Name")
        player_table.add_column("Chips")
        for player_id, player in players.items():
            player = player.get("player")
            player_table.add_row(str(player_id), player.name, f"{Chip.WHITE.name}: {player.stack.chips[Chip.WHITE.name]}")

        return (game_pot_table, game_cards_table, player_table)


        """
        summary different checkpoints

        player order
        player name
        chip count
        game pot
        community cards

        ask main player to press button when reay to continue
        """
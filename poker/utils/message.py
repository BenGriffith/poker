import time

from rich.table import Table
from rich.console import Console

from poker.utils.constants import Decision, Cash, COMPETITION, Chip, PlayerTable, GameTable
from poker.utils.exception import RangeException, CashException, GamePlayException
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
    

    def player_summary(self, players: dict) -> None:
        player_table = Table(title=PlayerTable.TITLE.value)
        player_table.add_column(PlayerTable.ORDER.value)
        player_table.add_column(PlayerTable.NAME.value)
        player_table.add_column(PlayerTable.CHIPS.value)
        player_table.add_column(PlayerTable.BLIND.value)
        for player_id, player in players.items():
            player = player.get("player")
            player_table.add_row(
                str(player_id), 
                player.name, 
                f"{Chip.WHITE.name}: {player.stack.chips[Chip.WHITE.name]}",
                "Big" if player_id == 1 else "Small"
                )
        console = Console()
        console.print("", player_table)
    

    def game_progression_prompt(self, name: str, not_ready: bool = None) -> None:
        try:
            if not_ready:
                player_response = input(f"{name}, how about now, are you ready? [yes/no] ")
            else:
                player_response = input(f"{name}, are you ready to continue? [yes/no] ")
            if player_response not in self.decision:
                raise GamePlayException
            if player_response in [Decision.N.value, Decision.NO.value]:
                time.sleep(5)
                self.game_progression_prompt(name, True)
        except GamePlayException:
            time.sleep(5)
            self.game_progression_prompt(name)
    

    def game_summary(self, pot: GameStack, community_cards: list) -> None:
        game_pot_table = Table(title=GameTable.POT.value)
        game_pot_table.add_column(GameTable.CHIP.value)
        game_pot_table.add_column(GameTable.COUNT.value)
        for chip, chip_count in pot.chips.items():
            game_pot_table.add_row(chip, str(chip_count))

        game_cards_table = Table(title=GameTable.COMMUNITY.value)
        game_cards_table.add_column(GameTable.COMMUNITY.value.split(" ")[1])
        for num, card in enumerate(community_cards, start=1):
            game_cards_table.add_row(f"{str(num)}: {card}")

        console = Console()
        console.print("", game_pot_table)
        console.print("", game_cards_table)
import time

from rich.table import Table
from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel


from poker.utils.constants import Decision, Cash, COMPETITION, Chip, PlayerTable, PLAYER_NAME
from poker.utils.exception import RangeException, CashException, GamePlayException
from poker.utils.chip import GameStack
from poker.utils.action import Action


class GameMessage:

    def __init__(self) -> None:
        self.cash_options = [item.value for item in Cash]
        self.decision = [item.value for item in Decision]


    def play(self) -> bool:
        player_response = input("Welcome to Texas hold'em! Would you like to play a game? [yes/no] ").lower()
        if player_response in [Decision.Y.value, Decision.YES.value]:
            return True
        return False
    
    
    def starting_cash(self) -> int:
        player_response = int(input(f"How much money would you like to start off with? {self.cash_options} "))
        if player_response not in self.cash_options:
            raise CashException
        return player_response
    
    
    def competition_count(self) -> int:
        count = int(input(f"How many players would you like to play against? {COMPETITION} "))
        if count not in COMPETITION:
            raise RangeException
        return count


    def competition_cash(self) -> int:
        cash = int(input(f"How much money should each player get? {self.cash_options[-2::]} "))
        if cash not in self.cash_options:
            raise CashException
        return cash
    
    
    def action(self, has_raise: bool, raise_amount: int) -> str:
        if has_raise:
            player_response = input(f"The bet was raised by {raise_amount}, what would you like to do? [{Action.CALL} or {Action.FOLD}] ")
        else:
            player_response = input(f"What would you like to do? [{Action.CHECK}, {Action.RAISE} or {Action.FOLD}] ")
        return player_response
    

    def action_taken(self, name: str, action: str, amount: int, possible_actions: list[str] = []) -> None:
        print(f"{name} decided to {action} {amount if action in possible_actions else ''}") 
    
    
    def increase(self) -> int:
        player_response = int(input(f"How much would you like to raise? "))
        return player_response
    

    def player_summary(self, players: dict) -> None:
        player_table = Table(title=PlayerTable.TITLE.value)
        player_table.add_column(PlayerTable.ORDER.value)
        player_table.add_column(PlayerTable.NAME.value)
        player_table.add_column(PlayerTable.CHIPS.value)
        player_table.add_column(PlayerTable.BLIND.value)
        player_table.add_column(PlayerTable.HAND.value)
        for player_id, player in players.items():
            player = player.get("player")
            player_table.add_row(
                str(player_id), 
                player.name, 
                f"{Chip.WHITE.name}: {player.stack.chips[Chip.WHITE.name]}",
                "Big" if player_id == 1 else "Small",
                " ".join(f"{card}" for card in player.hand) if player.name == PLAYER_NAME else "Hidden" 
                )
        console = Console()
        console.print("", player_table)
    

    def game_progression_prompt(self, not_ready: bool = None) -> None:
        try:
            if not_ready:
                player_response = input(f"How about now, are you ready? [yes/no] ")
            else:
                player_response = input(f"Are you ready to continue? [yes/no] ")
            if player_response not in self.decision:
                raise GamePlayException
            if player_response in [Decision.N.value, Decision.NO.value]:
                time.sleep(5)
                self.game_progression_prompt(True)
        except GamePlayException:
            time.sleep(5)
            self.game_progression_prompt()
    

    def game_summary(self, pot: GameStack, community_cards: list) -> None:
        game_pot = [Panel(f"Game Pot\n{key}: {value}") for key, value in pot.chips.items()]
        game_pot.extend(Panel(f"Card {card_number + 1}\n{community_cards[card_number]}") for card_number in range(len(community_cards)))
        console = Console()
        console.print(Columns(game_pot))
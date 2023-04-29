import time

from rich.table import Table
from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel


from poker.utils.constants import (
    Decision, 
    Cash, 
    COMPETITION, 
    PLAYER_NAME
)
from poker.utils.exception import (
    RangeException, 
    CashException, 
    GamePlayException, 
    NotReadyException, 
    InvalidActionException, 
    NegativeException
)
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
            if player_response not in [Action.CALL, Action.FOLD]:
                raise InvalidActionException
        else:
            player_response = input(f"What would you like to do? [{Action.CHECK}, {Action.RAISE} or {Action.FOLD}] ")
            if player_response not in [Action.CHECK, Action.RAISE, Action.FOLD]:
                raise InvalidActionException
        return player_response

    def action_taken(self, name: str, action: str, amount: int, possible_actions: list[str] = []) -> None:
        print(f"{name} decided to {action} {amount if action in possible_actions else ''}") 
    
    def increase(self) -> int:
        player_response = int(input(f"How much would you like to raise? "))
        if player_response < 0:
            raise NegativeException
        return player_response
    
    def player_summary(self, players: dict) -> None:
        player_table = Table(title="Player Summery")
        player_table.add_column("Order")
        player_table.add_column("Name")
        player_table.add_column("Chips")
        player_table.add_column("Blind")
        player_table.add_column("Hand")
        for player_id, player in players.items():
            player = player["player"]
            player_table.add_row(
                str(player_id), 
                player.name, 
                f"{GameStack.WHITE['name']}: {player.stack.chips[GameStack.WHITE['name']]}",
                "Big" if player_id == 1 else "Small",
                " ".join(f"{card}" for card in player.hand) if player.name == PLAYER_NAME else "Hidden" 
                )
        console = Console()
        console.print("", player_table)
    
    def game_progression_prompt(self, progress: bool = None) -> None:
        try:
            if progress:
                player_response = input(f"How about now, are you ready? [yes/no] ")
            else:
                player_response = input(f"Are you ready to continue? [yes/no] ")
            if player_response not in self.decision:
                raise GamePlayException
            if player_response in [Decision.N.value, Decision.NO.value]:
                raise NotReadyException
        except GamePlayException:
            time.sleep(5)
            self.game_progression_prompt()
        except NotReadyException:
            time.sleep(5)
            self.game_progression_prompt(progress=True)    

    def game_summary(self, pot: GameStack, community_cards: list) -> None:
        game_pot = [Panel(f"Game Pot\n{key}: {value}") for key, value in pot.chips.items()]
        game_pot.extend(Panel(f"Card {card_number + 1}\n{community_cards[card_number]}") for card_number in range(len(community_cards)))
        console = Console()
        console.print(Columns(game_pot))

    def showdown(self, winner: dict, pot: GameStack, players: dict) -> None:
        time.sleep(3)
        print(f"\nCongratulations {winner['name']}! You won ${pot.cash_equivalent()}!")
        for player in players.values():
            player = player["player"]
            print(f"{player.name}: {player.best_hand['best_hand']}")
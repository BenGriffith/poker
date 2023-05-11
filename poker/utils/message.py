from time import sleep

from rich.table import Table
from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel


from poker.utils.constants import (
    BetAction,
    Decision, 
    Cash,
    Blind, 
    COMPETITION, 
    PLAYER_NAME,
    GAME_DELAY,
    PLAYER_TABLE_COLUMNS,
    FIRST_PLAYER,
    HIDDEN,
    TIE
)
from poker.utils.exception import (
    RangeException, 
    CashException, 
    InvalidActionException, 
    NegativeException,
    InsufficientChipException
)
from poker.utils.chip import GameStack
from poker.utils.card import Card


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
        try:
            player_response = int(input(f"How much money would you like to start off with? {self.cash_options} "))
            if player_response not in self.cash_options:
                raise CashException
            return player_response
        except (ValueError, CashException) as err:
            print(err)
            player_response = self.starting_cash()
            return player_response
    
    def competition_count(self) -> int:
        try:
            count = int(input(f"How many players would you like to play against? {COMPETITION} "))
            if count not in COMPETITION:
                raise RangeException
            return count
        except (ValueError, RangeException) as err:
            print(err)
            count = self.competition_count()
            return count

    def raise_response(self, raise_amount: int, chip_count: int) -> str:
        try:
            player_response = input(f"The bet was raised by {raise_amount}, what would you like to do? [{BetAction.CALL.value} or {BetAction.FOLD.value}] ").lower()
            if player_response not in [BetAction.CALL.value, BetAction.FOLD.value]:
                raise InvalidActionException(valid_actions=[BetAction.CALL.value, BetAction.FOLD.value])
            if raise_amount > chip_count and player_response != BetAction.FOLD.value:
                raise InsufficientChipException(chip_count=chip_count)
            return player_response
        except (InvalidActionException, InsufficientChipException) as err:
            print(err)
            player_response = self.raise_response(raise_amount=raise_amount, chip_count=chip_count)
            return player_response

    def action(self, chip_count: int) -> str:
        if chip_count == 0:
            valid_actions = [BetAction.CHECK.value, BetAction.FOLD.value]
        else:
            valid_actions = [BetAction.CHECK.value, BetAction.RAISE.value, BetAction.FOLD.value]

        try:
            player_response = input(f"What would you like to do? [{', '.join(valid_actions)}] ").lower()
            if player_response not in valid_actions:
                raise InvalidActionException(valid_actions=valid_actions)
            return player_response
        except InvalidActionException as err:
            print(err)
            player_response = self.action()
            return player_response

    def action_taken(self, name: str, action: str, amount: int, possible_actions: list[str] = []) -> None:
        print(f"{name} decided to {action} {amount if action in possible_actions else ''}") 
    
    def increase(self, chip_count: int) -> int:
        try:
            player_response = int(input(f"How much would you like to raise? "))
            if player_response < 0:
                raise NegativeException
            if player_response > chip_count:
                raise InsufficientChipException(chip_count=chip_count)
            return player_response
        except (ValueError, NegativeException, InsufficientChipException) as err:
            print(err)
            player_response = self.increase(chip_count=chip_count)
            return player_response
    
    def player_summary(self, players: dict) -> None:
        player_table = Table(title="Player Summary")

        for column in PLAYER_TABLE_COLUMNS:
            player_table.add_column(column)

        for player_id, player in players.items():
            player = player["player"]
            player_order = str(player_id)
            player_name = player.name            
            player_chips = f"{GameStack.white['name']}: {player.stack.chips[GameStack.white['name']]}"
            player_blind = Blind.BIG.name if player_id == FIRST_PLAYER else Blind.SMALL.name

            player_pocket_cards = HIDDEN            
            if player.name == PLAYER_NAME or len(player.best_hand) > 1:
                player_pocket_cards = " ".join(f"{card}" for card in player.pocket_cards) 
            
            player_best_hand = ""
            short_name = ""
            if len(player.best_hand) > 1:
                player_best_hand = ", ".join(f"{card}" for card in player.best_hand["hand"]) 
                short_name = player.best_hand["short"]
            
            player_table.add_row(
                player_order, 
                player_name, 
                player_chips,
                player_blind,
                player_pocket_cards,
                player_best_hand,
                short_name
                )
            
        console = Console()
        console.print("", player_table)
    
    def game_progression_prompt(self, progress: bool = None) -> None:
        if progress:
            player_response = input(f"How about now, are you ready? [yes/no] ").lower()
        else:
            player_response = input(f"Are you ready to continue? [yes/no] ").lower()
            
        if player_response not in self.decision:
            sleep(GAME_DELAY)
            self.game_progression_prompt()
        if player_response in [Decision.N.value, Decision.NO.value]:
            sleep(GAME_DELAY)
            self.game_progression_prompt(progress=True)    

    def game_summary(self, pot: GameStack, community_cards: list) -> None:
        game_pot = [Panel(f"Game Pot\n{key}: {value}") for key, value in pot.chips.items()]
        game_pot.extend(Panel(f"Card {card_number + 1}\n{community_cards[card_number]}") for card_number in range(len(community_cards)))
        console = Console()
        console.print(Columns(game_pot))

    def showdown(self, winner: dict, pot: GameStack, players: dict, community_cards: list[Card]) -> None:
        sleep(GAME_DELAY)
        self.game_summary(pot=pot, community_cards=community_cards)
        sleep(GAME_DELAY)
        self.player_summary(players=players)
        sleep(GAME_DELAY)

        if len(winner) > TIE:
            winners = len(winner) // 2
            winnings = pot.cash_equivalent() / winners
            winners_names = []
            for key, value in winner.items():
                if "name" in key:
                    winners_names.append(value)
            winners_names_string = ", ".join(winners_names)
            print(f"\nWe have a tie! Congratulations {winners_names_string}! You each won ${winnings}!")
        
        if len(winner) == TIE:
            if winner["name"] == PLAYER_NAME:
                print(f"\nCongratulations you won ${pot.cash_equivalent()}!")
            else:
                print(f"\nCongratulations {winner['name']}! You won ${pot.cash_equivalent()}!")
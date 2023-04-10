import random
import logging
import time

from faker import Faker

from poker.utils.player import Dealer, Player, Computer
from poker.utils.action import Action
from poker.utils.chip import GameStack
from poker.utils.constants import Blind, Decision, Cash, COMPETITION, Chip
from poker.utils.exception import GamePlayException, NegativeException, RangeException, CashException


class GameMessage:

    def __init__(self) -> None:
        self.cash_options = [item.value for item in Cash]

    def greeting(self) -> None:
        print("Welcome to Texas hold'em! ")

    def play(self) -> bool:
        player_response = input("Would you like to play a game? [yes/no] ").lower()
        valid_response = [item.value for item in Decision]
        if player_response in [Decision.N.value, Decision.NO.value]:
            return False
        if player_response not in valid_response:
            # TODO logger
            raise GamePlayException
        return True
    
    def ask_name(self) -> str:
        player_response = input("What is your name? ").strip().capitalize()
        if player_response == "":
            return "Tron"
        return player_response
    
    def starting_cash(self, name: str) -> int:
        player_response = int(input(f"{name}, how much money would you like to start off with? {self.cash_options} "))
        if player_response <= 0:
            raise NegativeException
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
    
    def action(self, name: str) -> str:
        player_response = input(f"{name}, what would you like to do? ")
        return player_response
    
    def increase(self, name: str) -> int:
        player_response = int(input(f"{name}, how much would you like to raise? "))
        return player_response
    

class Game:

    def __init__(self, message: GameMessage, dealer: Dealer, player: Player) -> None:
        self.game_message = message
        self.dealer = dealer
        self.player = player
        self.action = Action
        self.pot = GameStack()
        self.competition = {}


    def start(self) -> None:
        while True:
            self.game_message.greeting()
            try:
                start_game = self.game_message.play()
                if start_game:
                    self.player.name = self.game_message.ask_name()
                    self.player.cash = self._setup_player_cash(self.player.name)
                else:
                    break
            except GamePlayException:
                time.sleep(5)
                break


    def _setup_player_cash(self, name: str) -> None:
        try:
            self.player.cash = self.game_message.starting_cash(name)
        except (ValueError, NegativeException, CashException):
            self._setup_player_cash(name)

        self.player.buy_chips(self.player.cash)
        self._setup_competition(name)


    def _setup_competition(self, name: str) -> None:
        try:
            competition_count, competition_cash = self.game_message.competition(name)
        except (ValueError, NegativeException, RangeException, CashException):
            self._setup_competition(name)

        self._create_competition(competition_count, competition_cash)
        self._game_order()
        self._preflop()


    def _create_competition(self, competitors: int, cash: int) -> None:
        fake = Faker()
        Faker.seed(0)        
        first_names = [fake.unique.first_name() for _ in range(500)]

        for _ in range(competitors):
            name = random.choice(first_names)
            self.competition[name] = Computer(name, cash)
    
        for player_info in self.competition.values():
            player_info.buy_chips(player_info.cash)


    def _game_order(self) -> None:
        self.game_order = {}
        players = [self.player] + list(self.competition.values())
        random.shuffle(players)
        for i, player in enumerate(players, start=1):
            self.game_order[i] = {"player": player}


    def _preflop(self) -> None:
        print("Shuffling Deck...")
        self.dealer.shuffle_deck()
        for card_number in range(1, 3):
            print(f"Dealing Card Number {card_number}")
            for order, players in self.game_order.items():
                player = players.get("player")
                print(f"Dealing card to {player.name}")
                self.dealer.deal_card(player)
        self._blind()
        self._theflop()


    def _blind(self) -> None:
        for order, player in self.game_order.items():
            _action = self.action(self.pot, player.get("player"))
            if order == 1:
                _action.blind(Chip.WHITE.name, Blind.BIG.value)
            else:
                _action.blind(Chip.WHITE.name, Blind.SMALL.value)


    def _action(self) -> None:
        action_log = {}
        increase = 0
        for order, player in self.game_order.items():
            player = player.get("player")

            if player.kind == "Computer":
                player_action = player.select_action(increase)
            else:
                player_action = self.game_message.action(player.name)
                if player_action == "increase":
                    increase = self.game_message.increase(player.name)

            if player_action == "fold":
                action_log[order] = player_action
                continue

            if player_action == "check":
                action_log[order] = player_action
                continue

            if player_action in ["increase", "call"]:
                increase = player.process_action(increase)
                action_log[order] = {player_action: increase}
                self.pot.increment(Chip.WHITE.name, increase)

        self._remove_fold_players(action_log)

    def _process_checks_to_calls(self, log):
        pass


    def _remove_fold_players(self, log: dict) -> None:
        breakpoint()
        for order, action in log.items():
            if action == "fold":
                del self.game_order[order]
            

    def _theflop(self) -> None:
        print("Here comes the flop...")
        self.dealer.deck.cards.pop()
        for card_number in range(1, 4):
            self.dealer.deal_card(self.dealer)
            print(f"Community card {card_number} is {self.dealer.hand[card_number - 1]}")
        self._action()
        self._theturn()


    def _theturn(self) -> None:
        self.dealer.deck.cards.pop()
        self.dealer.deal_card(self.dealer)
        self._theriver()


    def _theriver(self) -> None:
        self.dealer.deck.cards.pop()
        self.dealer.deal_card(self.dealer)
        self._showdown()


    def _showdown(self) -> None:
        pass # declare winner
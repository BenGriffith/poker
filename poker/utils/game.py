import random
import logging
from collections import defaultdict

from faker import Faker

from poker.utils.deck import Deck, Card
from poker.utils.player import Dealer, Player, Computer
from poker.utils.action import Action
from poker.utils.chip import GameStack
from poker.utils.constants import Blind, Decision, COMPETITION
from poker.utils.exception import GamePlayException, NegativeException, RangeException


class GameMessage:

    def __init__(self) -> None:
        pass

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
        player_response = int(input(f"{name}, how much money would you like to start off with? "))
        if player_response <= 0:
            raise NegativeException
        return player_response
    
    def competition(self, name: str) -> int:
        player_response = int(input(f"{name}, how many players would you like to play against? [1 to 3] "))
        if player_response not in COMPETITION:
            raise RangeException
        return player_response


class Game:

    def __init__(self, message: GameMessage, dealer: Dealer, player: Player) -> None:
        self.game_message = message
        self.dealer = dealer
        self.player = player
        self.action = Action
        self.pot = GameStack()

    def start(self) -> None:
        while True:
            self.game_message.greeting()
            try:
                start_game = self.game_message.play()
                if start_game:
                    player_name = self.game_message.ask_name()
                    self.player.name = player_name
                    self.player.cash = self._setup_player_cash(player_name)
                else:
                    break
            except GamePlayException:
                break

    def _setup_player_cash(self, name: str) -> None:
        try:
            player_cash = self.game_message.starting_cash(name)
            self.player.cash = player_cash
            self._setup_competition(name)
        except (ValueError, NegativeException):
            self.setup_player()

    def _create_competition(self, competitors: int) -> None:
        fake = Faker()
        Faker.seed(0)        

        first_names = [fake.unique.first_name() for _ in range(500)]
        self.competition = {}

        for _ in range(competitors):
            name = random.choice(first_names)
            self.competition[name] = Computer(name, 10)

    def _setup_competition(self, name: str) -> None:
        try:
            player_response = self.game_message.competition(name)
            self._create_competition(player_response)
            self._game_order()
        except (ValueError, NegativeException, RangeException):
            self.setup_competition()

    def _game_order(self):
        self.game_order = {}
        for i, name in enumerate([self.player.name] + list(self.competition.keys()), start=1):
            self.game_order[name] = {"order": i}



        # self.dealer.shuffle_deck()

        # for _ in range(2):
        #     self.dealer.deal_card(self.player)

        # self.dealer.deck.cards.pop()

        # for _ in range(3):
        #     self.dealer.deal_card(self.dealer)

        # self.dealer.deck.cards.pop()

        # self.dealer.deal_card(self.dealer)

        # self.dealer.deck.cards.pop()

        # self.dealer.deal_card(self.dealer)


import random
import logging
import time

from faker import Faker

from poker.utils.player import Dealer, Player, Computer
from poker.utils.action import Action
from poker.utils.chip import GameStack
from poker.utils.message import GameMessage
from poker.utils.constants import Blind, Decision, Cash, COMPETITION, Chip
from poker.utils.exception import NegativeException, RangeException, CashException
    

class Game:

    def __init__(self, message: GameMessage, dealer: Dealer, player: Player) -> None:
        self.message = message
        self.dealer = dealer
        self.player = player
        self.action = Action
        self.pot = GameStack()
        self.competition = {}


    def start(self) -> None:
        while True:
            try:
                start_game = self.message.play()
                if start_game:
                    self.player.name = self.message.ask_name()
                    self.player.cash = self._setup_player_cash(self.player.name)
                else:
                    break
            except:
                pass # logger
                break


    def _setup_player_cash(self, name: str) -> None:
        try:
            self.player.cash = self.message.starting_cash(name)
        except (ValueError, NegativeException, CashException):
            self._setup_player_cash(name)

        self.player.buy_chips(self.player.cash)
        self._setup_competition(name)


    def _setup_competition(self, name: str) -> None:
        try:
            competition_count, competition_cash = self.message.competition(name)
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


    def _action(self) -> tuple:
        action_log = {}
        raise_amount = 0
        has_raise = False
        for order, player in self.game_order.items():
            player = player.get("player")

            if player.kind == "Computer":
                player_action = player.select_action(raise_amount)
            else:

                player_action = self.message.action(player.name, has_raise, raise_amount)
                if player_action == "call":
                    call_amount = player.process_action(raise_amount)
                    action_log[order] = {player_action: call_amount}
                    self.pot.increment(Chip.WHITE.name, call_amount)  
            
                if player_action == "raise":
                    raise_amount = self.message.increase(player.name)

            if player_action == "fold":
                action_log[order] = player_action
                continue

            if player_action == "check":
                action_log[order] = player_action
                continue

            if player_action == "raise":
                has_raise = True
                raise_amount = player.process_action(raise_amount)
                action_log[order] = {player_action: raise_amount}
                self.pot.increment(Chip.WHITE.name, raise_amount)

            if player_action == "call":
                call_amount = player.process_action(raise_amount)
                action_log[order] = {player_action: call_amount}
                self.pot.increment(Chip.WHITE.name, call_amount)             

        return action_log


    def _process_checks_to_calls(self, log: dict) -> None:
        call_amount = 0
        players_with_check_action = []
        for order, action in log.items():
            if action == "check":
                players_with_check_action.append(order)
        for order, action in log.items():
            if isinstance(action, dict):
                call_amount = [value for value in action.values()][0]
                break

        if call_amount > 0:
            for player_id in players_with_check_action:

                player = self.game_order[player_id].get("player")
                if player.kind == "Computer":
                    player_action = player.select_action(call_amount)
                    if player_action == "fold":
                        log[player_id] = player_action
                    if player_action == "call":
                        call_amount = player.process_action(call_amount)
                        log[player_id] = {player_action: call_amount}
                        self.pot.increment(Chip.WHITE.name, call_amount)
                else:
                    player_action = self.message.action(player.name, True, call_amount)
                    if player_action == "fold":
                        log[player_id] = player_action
                    if player_action == "call":
                        call_amount = player.process_action(call_amount)
                        log[player_id] = {player_action: call_amount}
                        self.pot.increment(Chip.WHITE.name, call_amount)


    def _remove_fold_players(self, log: dict) -> None:
        for order, action in log.items():
            if action == "fold":
                del self.game_order[order]
            

    def _theflop(self) -> None:
        print("Here comes the flop...")
        self.dealer.deck.cards.pop()
        for card_number in range(1, 4):
            self.dealer.deal_card(self.dealer)
            print(f"Community card {card_number} is {self.dealer.hand[card_number - 1]}")
        action_log = self._action()
        self._process_checks_to_calls(action_log)
        self._remove_fold_players(action_log)
        self._theturn()


    def _theturn(self) -> None:
        print("Here comes the turn...")
        self.dealer.deck.cards.pop()
        self.dealer.deal_card(self.dealer)
        action_log = self._action()
        self._process_checks_to_calls(action_log)
        self._remove_fold_players(action_log)
        self._theriver()


    def _theriver(self) -> None:
        print("Here comes the river...")
        self.dealer.deck.cards.pop()
        self.dealer.deal_card(self.dealer)
        action_log = self._action()
        self._process_checks_to_calls(action_log)
        self._remove_fold_players(action_log)
        self._showdown()


    def _showdown(self) -> None:
        breakpoint()
        pass # declare winner
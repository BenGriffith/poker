import random
import logging
import time

from faker import Faker

from poker.utils.player import Dealer, Player, Computer
from poker.utils.action import Action
from poker.utils.chip import GameStack
from poker.utils.message import GameMessage
from poker.utils.constants import Blind, Chip, PLAYER_NAME
from poker.utils.exception import RangeException, CashException
    

class Game:

    def __init__(self, message: GameMessage, dealer: Dealer, player: Player) -> None:
        self.message = message
        self.dealer = dealer
        self.player = player
        self.pot = GameStack()
        self.action = Action(self.pot)
        self.competition = {}


    def start(self) -> None:
        while True:
            try:
                start_game = self.message.play()
                if start_game:
                    self.player.name = PLAYER_NAME
                    self.player.cash = self._setup_player_cash()
                    breakpoint()
                else:
                    break
            except:
                pass # setup logger
                break


    def _setup_player_cash(self) -> None:
        try:
            self.player.cash = self.message.starting_cash()
        except (ValueError, CashException):
            self._setup_player_cash()
        self.player.buy_chips(self.player.cash)
        self._setup_competition_count()


    def _setup_competition_count(self) -> None:
        try:
            competition_count = self.message.competition_count()
        except (ValueError, RangeException):
            self._setup_competition_count()
        self._setup_competition_cash(competition_count)


    def _setup_competition_cash(self, competition_count: int) -> None:
        try:
            competition_cash = self.message.competition_cash()
        except (ValueError, CashException):
            self._setup_competition_cash(competition_count)
        self._create_competition(competition_count, competition_cash)


    def _setup_competition_names(self) -> None:
        fake = Faker()
        Faker.seed(0)        
        return [fake.unique.first_name() for _ in range(500)]


    def _create_competition(self, count: int, cash: int) -> None:
        names = self._setup_competition_names()

        for _ in range(count):
            player_name = random.choice(names)
            self.competition[player_name] = Computer(player_name, cash)

        for player in self.competition.values():
            player.buy_chips(player.cash)
        self._player_order()
        self._preflop()


    def _player_order(self) -> None:
        self.player_order = {}
        players = [self.player] + list(self.competition.values())
        random.shuffle(players)
        for player_id, player in enumerate(players, start=1):
            self.player_order[player_id] = {"player": player}
        time.sleep(1)
        self.message.player_summary(self.player_order)
        self.message.game_progression_prompt()


    def _preflop(self) -> None:
        print("Shuffling Deck...")
        self.dealer.shuffle_deck()
        time.sleep(1)
        for card_number in range(1, 3):
            print(f"Dealing {'First' if card_number == 1 else 'Second'} Card")
            time.sleep(1)
            for player in self.player_order.values():
                current_player = player.get("player")
                print(f"Dealt card to {current_player.name}")
                self.dealer.deal_card(current_player)
                time.sleep(1)
            time.sleep(1)
        self._blind()


    def _blind(self) -> None:
        for player_id, player in self.player_order.items():
            self.action.person = player.get("player")
            if player_id == 1:
                self.action.blind(Chip.WHITE.name, Blind.BIG.value)
            else:
                self.action.blind(Chip.WHITE.name, Blind.SMALL.value)
        time.sleep(2)
        self.message.player_summary(self.player_order)
        time.sleep(2)
        self.message.game_progression_prompt()
        self._theflop()


    def _action(self) -> tuple:
        action_log = {}
        raise_amount = 0
        has_raise = False
        for order, player in self.player_order.items():
            player = player.get("player")

            if player.kind == "Computer":
                player_action = player.select_action(raise_amount)
            else:

                player_action = self.message.action(player.name, has_raise, raise_amount)
                if player_action == self.action.CALL:
                    call_amount = player.process_action(raise_amount)
                    action_log[order] = {player_action: call_amount}
                    self.pot.increment(Chip.WHITE.name, call_amount)  
            
                if player_action == self.action.RAISE:
                    raise_amount = self.message.increase(player.name)

            if player_action == self.action.FOLD:
                action_log[order] = player_action
                continue

            if player_action == self.action.CHECK:
                action_log[order] = player_action
                continue

            if player_action == self.action.RAISE:
                has_raise = True
                raise_amount = player.process_action(raise_amount)
                action_log[order] = {player_action: raise_amount}
                self.pot.increment(Chip.WHITE.name, raise_amount)

            if player_action == self.action.CALL:
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

                player = self.player_order[player_id].get("player")
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
                del self.player_order[order]
            

    def _theflop(self) -> None:
        print("Here comes the flop...")
        self.dealer.deck.cards.pop()
        for _ in range(1, 4):
            self.dealer.deal_card(self.dealer)
        time.sleep(2)
        self.message.game_summary(self.pot, self.dealer.hand)
        time.sleep(2)
        self.message.game_progression_prompt()
        self._process_betting()


    def _process_betting(self) -> None:
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
import random
import logging
import time
from itertools import combinations
from collections import Counter

from faker import Faker

from poker.utils.player import Dealer, Player, Computer
from poker.utils.action import Action
from poker.utils.chip import GameStack
from poker.utils.message import GameMessage
from poker.utils.constants import Blind, Chip, PLAYER_NAME, FaceCards
from poker.utils.exception import RangeException, CashException, InvalidActionException
    

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
                    self._setup_player_cash()
                    breakpoint()
                else:
                    break
            except:
                raise # setup logger
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
        print("\nShuffling Deck...")
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
        print("\nProcessing Big and Small Blinds...")
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


    def _select_player_action(self, has_raise: bool, raise_amount: int) -> str:
        try:
            player_action = self.message.action(has_raise, raise_amount)
        except InvalidActionException:
            player_action = self._select_player_action(has_raise, raise_amount)
        return player_action


    def _action(self) -> dict:
        print("\nProcessing betting...")
        action_log = {}
        raise_amount = 0
        has_raise = False
        time.sleep(2)
        for order, player in self.player_order.items():
            player = player.get("player")

            if player.kind == "Computer":
                player_action = player.select_action(raise_amount)
            else:
                player_action = self._select_player_action(has_raise, raise_amount)
                if player_action == self.action.CALL:
                    raise_amount = player.process_action(raise_amount)
                    action_log[order] = {player_action: raise_amount}
                    self.pot.increment(Chip.WHITE.name, raise_amount)  
                    self.message.action_taken(player.name, player_action, raise_amount, [self.action.RAISE, self.action.CALL])
                    time.sleep(2) 
                    continue
            
                if player_action == self.action.RAISE:
                    raise_amount = self.message.increase()

            if player_action in [self.action.FOLD, self.action.CHECK]:
                action_log[order] = player_action
                self.message.action_taken(player.name, player_action, raise_amount, [self.action.RAISE, self.action.CALL])
                time.sleep(2) 
                continue

            if player_action == self.action.RAISE:
                has_raise = True
                raise_amount = player.process_action(raise_amount)
                action_log[order] = {player_action: raise_amount}
                self.pot.increment(Chip.WHITE.name, raise_amount)

            if player_action == self.action.CALL:
                raise_amount = player.process_action(raise_amount)
                action_log[order] = {player_action: raise_amount}
                self.pot.increment(Chip.WHITE.name, raise_amount)     

            self.message.action_taken(player.name, player_action, raise_amount, [self.action.RAISE, self.action.CALL])
            time.sleep(2)     

        return action_log


    def _call_amount(self, log: dict) -> int:
        call_amount = 0
        for action in log.values():
            if isinstance(action, dict):
                call_amount = [value for value in action.values()][0]
                break
        return call_amount


    def _players_with_check(self, log: dict) -> list:
        players_with_check = []
        for order, action in log.items():
            if action == self.action.CHECK:
                players_with_check.append(order)
        return players_with_check


    def _process_player_checks_to_calls(self, player_id: int, player: Player, call_amount: int, log: dict) -> tuple:
        if player.kind == "Computer":
            player_action = player.select_action(call_amount)
        if player.kind == "Player":
            player_action = self._select_player_action(True, call_amount)
        if player_action == self.action.FOLD:
            log[player_id] = player_action
        if player_action == self.action.CALL:
            call_amount = player.process_action(call_amount)
            log[player_id] = {player_action: call_amount}
            self.pot.increment(Chip.WHITE.name, call_amount)
        return (player_action, log)


    def _process_checks_to_calls(self, log: dict) -> None:
        call_amount = self._call_amount(log)
        players_with_check = self._players_with_check(log)

        if call_amount > 0:
            for player_id in players_with_check:
                player = self.player_order[player_id].get("player")
                player_action, log = self._process_player_checks_to_calls(player_id, player, call_amount, log)
                self.message.action_taken(player.name, player_action, call_amount, [self.action.CALL])
                time.sleep(2)  


    def _remove_fold_players(self, log: dict) -> None:
        for order, action in log.items():
            if action == "fold":
                del self.player_order[order]
            

    def _theflop(self) -> None:
        print("\nHere comes the flop...")
        self.dealer.deck.cards.pop()
        for _ in range(1, 4):
            self.dealer.deal_card(self.dealer)
        time.sleep(3)
        self.message.game_summary(self.pot, self.dealer.hand)
        time.sleep(3)
        self.message.game_progression_prompt()
        self._process_betting()
        self._theturn()


    def _process_betting(self) -> None:
        action_log = self._action()
        self._process_checks_to_calls(action_log)
        self._remove_fold_players(action_log)


    def _theturn(self) -> None:
        print("\nHere comes the turn...")
        self.dealer.deck.cards.pop()
        self.dealer.deal_card(self.dealer)
        time.sleep(3)
        self.message.game_summary(self.pot, self.dealer.hand)
        time.sleep(3)
        self.message.player_summary(self.player_order)
        time.sleep(3)
        self.message.game_progression_prompt()
        self._process_betting()
        self._theriver()


    def _theriver(self) -> None:
        print("\nHere comes the river...")
        self.dealer.deck.cards.pop()
        self.dealer.deal_card(self.dealer)
        time.sleep(3)
        self.message.game_summary(self.pot, self.dealer.hand)
        time.sleep(3)
        self.message.player_summary(self.player_order)
        time.sleep(3)
        self.message.game_progression_prompt()
        self._process_betting()
        self._showdown()


    def _showdown(self) -> None:
        for player in self.player_order.values():
            player = player.get("player")
            self._process_player_hands(player)
    
    
    def _process_player_hands(self, person):
        """
        poker_hands
        create hand combinations between player hand and community hand
        compare against poker hands 
        fetch best hand
        compare against other poker players

        functions to evaluate whether any of the following apply, if they do where are they stored
        three of a kind
        two pair
        one pair
        high card

        """




        player_best_hand = person.hand.copy()
        player_best_hand.extend(self.dealer.hand)
        player_hand_combinations = list(combinations(player_best_hand, 5))
        for hand in player_hand_combinations:
            hand = self._process_player_hand(hand)
            self._process_best_hand(hand, person)
        breakpoint()

        

    def _process_best_hand(self, hand: Counter, person) -> None:
        if hand.most_common()[0][1] == 3:
            if person.best_hand:
                if int(person.best_hand["best_hand"][0]) < int(hand.most_common()[0][0]):
                    person.best_hand = {"hand": hand, "best_hand": hand.most_common()[0]}
            else:
                person.best_hand = {"hand": hand, "best_hand": hand.most_common()[0]}
        


        elif hand.most_common()[0][1] == 2 and hand.most_common()[1][1] == 2:
            if person.best_hand:
                old_hand = [int(pair[0]) for pair in person.best_hand["best_hand"]]
                new_hand = [int(pair[0]) for pair in hand.most_common()[:2]]
                old_hand.sort()
                new_hand.sort()
                new_count = 0
                for new, old in list(zip(new_hand, old_hand)):
                    if new > old:
                        new_count += 1
                if new_count == 2:
                    person.best_hand = {"hand": hand, "best_hand": hand.most_common()[:2]}
            else:
                person.best_hand = {"hand": hand, "best_hand": hand.most_common()[:2]}
        


        elif hand.most_common()[0][1] == 2:
            if person.best_hand:
                if int(person.best_hand["best_hand"][0]) < int(hand.most_common()[0][0]):
                    person.best_hand = {"hand": hand, "best_hand": hand.most_common()[0]}
            else:
                person.best_hand = {"hand": hand, "best_hand": hand.most_common()[0]}
        
        else:
            if person.best_hand:
                if int(person.best_hand["best_hand"][0]) < int(hand.most_common()[0][0]):
                    person.best_hand = {"hand": hand, "best_hand": hand.most_common()[0]}
            else:
                person.best_hand = {"hand": hand, "best_hand": hand.most_common()[0]}


    def _process_player_hand(self, hand: tuple) -> Counter:
        counter = Counter()
        for card in hand:
            counter.update(str(card.rank) if isinstance(card.rank, int) else [str(card.value())])
        return counter
        




import random
from time import sleep
from itertools import combinations
from collections import Counter, defaultdict
from typing import Union

from faker import Faker

from poker.utils.player import Dealer, Player, Computer
from poker.utils.card import Card
from poker.utils.action import Action
from poker.utils.chip import GameStack
from poker.utils.message import GameMessage
from poker.utils.constants import Blind, PLAYER_NAME, GAME_DELAY
from poker.utils.exception import (
    RangeException, 
    CashException, 
    InvalidActionException, 
    NegativeException,
    InsufficientChipException
)
    

class Game:

    def __init__(self, message: GameMessage, dealer: Dealer, player: Player) -> None:
        self.message = message
        self.dealer = dealer
        self.player = player
        self.pot = GameStack()
        self.action = Action(self.pot)
        self.competition = {}

    def start(self) -> None:
        try:
            start_game = self.message.play()
            if start_game:
                self.player.name = PLAYER_NAME
                self._setup_player_cash()
                sleep(GAME_DELAY)
                print("\nThanks for playing! Hope to see you again soon!")
            else:
                sleep(GAME_DELAY)
                print("\nThanks for stopping by! Hope to see you again soon!")
        except:
            pass # setup logger

    def _setup_player_cash(self) -> None:
        try:
            self.player.cash = self.message.starting_cash()
        except (ValueError, CashException):
            self._setup_player_cash()
        self.player.buy_chips(value=self.player.cash)
        self._setup_competition_count()

    def _setup_competition_count(self) -> None:
        try:
            competition_count = self.message.competition_count()
        except (ValueError, RangeException):
            self._setup_competition_count()
        self._setup_competition_cash(competition_count=competition_count)

    def _setup_competition_cash(self, competition_count: int) -> None:
        try:
            competition_cash = self.message.competition_cash()
        except (ValueError, CashException):
            self._setup_competition_cash(competition_count=competition_count)
        self._create_competition(count=competition_count, cash=competition_cash)

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
            player.buy_chips(value=player.cash)
        self._player_order()
        self._preflop()

    def _player_order(self) -> None:
        self.player_order = {}
        players = [self.player] + list(self.competition.values())
        random.shuffle(players)
        for player_id, player in enumerate(players, start=1):
            self.player_order[player_id] = {"player": player}
        sleep(GAME_DELAY)
        self.message.player_summary(self.player_order)
        sleep(GAME_DELAY)
        self.message.game_progression_prompt()

    def _preflop(self) -> None:
        print("\nShuffling Deck...")
        self.dealer.shuffle_deck()
        sleep(GAME_DELAY)
        for card_number in range(1, 3):
            print(f"Dealing {'First' if card_number == 1 else 'Second'} Card")
            sleep(GAME_DELAY)
            for player in self.player_order.values():
                current_player = player["player"]
                print(f"Dealt card to {current_player.name}")
                self.dealer.deal_card(person=current_player)
                sleep(GAME_DELAY)
            sleep(GAME_DELAY)
        self._blind()        

    def _blind(self) -> None:
        print("\nProcessing Big and Small Blinds...")
        for player_id, player in self.player_order.items():
            self.action.person = player["player"]
            if player_id == 1:
                self.action.blind(chip=self.player.stack.WHITE["name"], value=Blind.BIG.value)
            else:
                self.action.blind(chip=self.player.stack.WHITE["name"], value=Blind.SMALL.value)
        sleep(GAME_DELAY)
        self.message.player_summary(players=self.player_order)
        sleep(GAME_DELAY)
        self.message.game_progression_prompt()
        self._theflop()

    def _select_player_action(self, has_raise: bool, raise_amount: int) -> str:
        try:
            player_action = self.message.action(has_raise=has_raise, raise_amount=raise_amount)
        except InvalidActionException:
            player_action = self._select_player_action(has_raise=has_raise, raise_amount=raise_amount)
        return player_action

    def _select_raise_amount(self) -> int:
        chip_count = self.player.stack.chips["White"]
        try:
            raise_amount = self.message.increase(chip_count=chip_count)
        except (ValueError, NegativeException):
            raise_amount = self._select_raise_amount()
        except InsufficientChipException:
            self.message.different_amount(chip_count=chip_count)
            raise_amount = self._select_raise_amount()
        return raise_amount            

    def _process_player_action(self) -> dict:
        print("\nProcessing betting...")
        action_log = {}
        has_raise = False
        raise_amount = 0

        sleep(GAME_DELAY)

        for order, player in self.player_order.items():
            player = player["player"]

            if player.kind == self.player.COMPUTER:
                player_action = player.select_action(raise_amount)

            if player.kind == self.player.PLAYER:
                player_action = self._select_player_action(has_raise, raise_amount)
                if player_action == self.action.RAISE:
                    raise_amount = self._select_raise_amount()
            
            if player_action in [self.action.FOLD, self.action.CHECK]:
                action_log[order] = player_action

            if player_action == self.action.RAISE:
                has_raise = True
                raise_amount = player.process_bet(raise_amount)
                action_log[order] = {player_action: raise_amount}
                self.pot.increment(self.player.stack.WHITE["name"], raise_amount)

            if player_action == self.action.CALL:
                raise_amount = player.process_bet(raise_amount)
                action_log[order] = {player_action: raise_amount}
                self.pot.increment(self.player.stack.WHITE["name"], raise_amount)     

            self.message.action_taken(player.name, player_action, raise_amount, [self.action.RAISE, self.action.CALL])
            sleep(GAME_DELAY)

        return action_log
    
    def _process_checks_to_calls(self, action_log: dict) -> None:
        call_amount = self._call_amount(action_log=action_log)
        players_with_check = self._players_with_check(action_log=action_log)

        if call_amount > 0:
            for player_id in players_with_check:
                player = self.player_order[player_id]["player"]

                player_action, action_log = self._process_player_checks_to_calls(
                    player_id=player_id,
                    player=player,
                    call_amount=call_amount,
                    action_log=action_log
                )

                self.message.action_taken(
                    name=player.name,
                    action=player_action,
                    amount=call_amount,
                    possible_actions=[self.action.CALL]
                )

                sleep(GAME_DELAY)

    def _call_amount(self, action_log: dict) -> int:
        call_amount = 0
        for action in action_log.values():
            if isinstance(action, dict):
                call_amount = [value for value in action.values()][0]
                break
        return call_amount

    def _players_with_check(self, action_log: dict) -> list:
        players_with_check = []
        for order, action in action_log.items():
            if action == self.action.CHECK:
                players_with_check.append(order)
        return players_with_check

    def _process_player_checks_to_calls(self, player_id: int, player: Player, call_amount: int, action_log: dict) -> tuple:
        if player.kind == self.player.COMPUTER:
            player_action = player.select_action(raise_amount=call_amount)

        if player.kind == self.player.PLAYER:
            player_action = self._select_player_action(has_raise=True, raise_amount=call_amount)

        if player_action == self.action.FOLD:
            action_log[player_id] = player_action

        if player_action == self.action.CALL:
            call_amount = player.process_bet(raise_amount=call_amount)
            action_log[player_id] = {player_action: call_amount}
            self.pot.increment(chip=self.player.stack.WHITE["name"], quantity=call_amount)

        return (player_action, action_log)

    def _remove_fold_players(self, action_log: dict) -> None:
        for order, action in action_log.items():
            if action == Action.FOLD:
                del self.player_order[order]

    def _theflop(self) -> None:
        print("\nHere comes the flop...")
        self.dealer.deck.cards.pop()
        for _ in range(1, 4):
            self.dealer.deal_card(person=self.dealer)
        sleep(GAME_DELAY)
        self.message.game_summary(pot=self.pot, community_cards=self.dealer.hand)
        sleep(GAME_DELAY)
        self.message.game_progression_prompt()
        self._process_betting()
        self._theturn()

    def _process_betting(self) -> None:
        action_log = self._process_player_action()
        self._process_checks_to_calls(action_log=action_log)
        self._remove_fold_players(action_log=action_log)

    def _theturn(self) -> None:
        print("\nHere comes the turn...")
        self.dealer.deck.cards.pop()
        self.dealer.deal_card(person=self.dealer)
        sleep(GAME_DELAY)
        self.message.game_summary(pot=self.pot, community_cards=self.dealer.hand)
        sleep(GAME_DELAY)
        self.message.player_summary(players=self.player_order)
        sleep(GAME_DELAY)
        self.message.game_progression_prompt()
        self._process_betting()
        self._theriver()

    def _theriver(self) -> None:
        print("\nHere comes the river...")
        self.dealer.deck.cards.pop()
        self.dealer.deal_card(person=self.dealer)
        sleep(GAME_DELAY)
        self.message.game_summary(pot=self.pot, community_cards=self.dealer.hand)
        sleep(GAME_DELAY)
        self.message.player_summary(players=self.player_order)
        sleep(GAME_DELAY)
        self.message.game_progression_prompt()
        self._process_betting()
        self._showdown()
    
    def _showdown(self) -> None:
        for player in self.player_order.values():
            player = player["player"]
            self._process_player_hands(person=player)
        winner = self._winner()
        winner = self._tie(winner=winner)
        print("\nFinal Results...")
        self.message.showdown(winner=winner, pot=self.pot, players=self.player_order, community_cards=self.dealer.hand)
    
    def _process_player_hands(self, person: Union[Player, Computer]) -> None:
        player_best_hand = person.pocket_cards.copy()
        player_best_hand.extend(self.dealer.hand)
        player_hand_combinations = list(combinations(player_best_hand, 5))
        player_hand_rankings = {
            "three_kind": False,
            "two_pair": False,
            "pair": False,
        }
        for hand in player_hand_combinations:
            counter_hand = self._convert_hand_to_counter(hand=hand)
            self._process_best_hand(hand=hand, counter_hand=counter_hand, person=person, hand_rankings=player_hand_rankings)

    def _convert_hand_to_counter(self, hand: tuple) -> Counter:
        counter = Counter()
        for card in hand:
            counter.update([int(card.rank)] if isinstance(card.rank, int) else [card.value()])
        return counter

    def _process_best_hand(self, hand: list[Card], counter_hand: Counter, person: Union[Player, Computer], hand_rankings: dict) -> None:

        top_frequency = counter_hand.most_common()[0][1]
        second_frequency = counter_hand.most_common()[1][1]

        if top_frequency == 3: # three of a kind
            self._three_kind(hand=hand, counter_hand=counter_hand, person=person, hand_rankings=hand_rankings)

        if top_frequency == 2 and second_frequency == 2 and not hand_rankings["three_kind"]:
            self._two_pair(hand=hand, counter_hand=counter_hand, person=person, hand_rankings=hand_rankings)
        
        if top_frequency == 2 and not hand_rankings["three_kind"] and not hand_rankings["two_pair"]:
            self._pair(hand=hand, counter_hand=counter_hand, person=person, hand_rankings=hand_rankings)
        
        if not hand_rankings["three_kind"] and not hand_rankings["two_pair"] and not hand_rankings["pair"]:
            self._high_card(hand=hand, counter_hand=counter_hand, person=person)

    def _three_kind(self, hand: list[Card], counter_hand: Counter, person: Union[Player, Computer], hand_rankings: dict) -> None:
        if person.best_hand and not hand_rankings["two_pair"] and not hand_rankings["pair"]:
            previous_best_hand_value = person.best_hand["best_hand"][0]
            current_best_hand_value = counter_hand.most_common()[0][0]
            if previous_best_hand_value < current_best_hand_value:
                person.best_hand = {
                    "hand": hand, 
                    "counter_hand": counter_hand, 
                    "best_hand": counter_hand.most_common()[0], 
                    "short": "Three of a Kind"
                    }
        else:
            person.best_hand = {
                "hand": hand, 
                "counter_hand": counter_hand, 
                "best_hand": counter_hand.most_common()[0], 
                "short": "Three of a Kind"
                }
        hand_rankings["three_kind"] = True

    def _two_pair(self, hand: list[Card], counter_hand: Counter, person: Union[Player, Computer], hand_rankings: dict) -> None:
        if isinstance(person.best_hand, list):
            old_hand = sorted([pair[0] for pair in person.best_hand["best_hand"]])
            new_hand = sorted([pair[0] for pair in counter_hand.most_common()[:2]])
            greater_count = 0
            equal_count = 0
            for new, old in list(zip(new_hand, old_hand)):
                if new > old:
                    greater_count += 1
                if new == old:
                    equal_count += 1
            if greater_count == 2 or (greater_count == 1 and equal_count == 1):
                person.best_hand = {
                    "hand": hand, 
                    "counter_hand": counter_hand, 
                    "best_hand": counter_hand.most_common()[:2], 
                    "short": "Two Pair"
                    }
        else:
            person.best_hand = {
                "hand": hand, 
                "counter_hand": counter_hand, 
                "best_hand": counter_hand.most_common()[:2], 
                "short": "Two Pair"
                }
        hand_rankings["two_pair"] = True

    def _pair(self, hand: list[Card], counter_hand: Counter, person: Union[Player, Computer], hand_rankings: dict) -> None:
        if person.best_hand:
            previous_best_hand_value = person.best_hand["best_hand"][0]
            current_best_hand_value = counter_hand.most_common()[0][0]
            if previous_best_hand_value < current_best_hand_value:
                person.best_hand = {
                    "hand": hand, 
                    "counter_hand": counter_hand, 
                    "best_hand": counter_hand.most_common()[0], 
                    "short": "Pair"
                    }
        else:
            person.best_hand = {
                "hand": hand, 
                "counter_hand": counter_hand, 
                "best_hand": counter_hand.most_common()[0], 
                "short": "Pair"
                }
        hand_rankings["pair"] = True

    def _high_card(self, hand: list[Card], counter_hand: Counter, person: Union[Player, Computer]) -> None:
        top_card = sorted(counter_hand.most_common(), reverse=True)
        if person.best_hand:
            previous_best_hand_value = person.best_hand["best_hand"][0]
            current_best_hand_value = top_card[0][0]
            if previous_best_hand_value < current_best_hand_value:
                person.best_hand = {
                    "hand": hand, 
                    "counter_hand": counter_hand, 
                    "best_hand": top_card[0], 
                    "short": "High Card"
                    }
        else:
            person.best_hand = {
                "hand": hand, 
                "counter_hand": counter_hand, 
                "best_hand": top_card[0], 
                "short": "High Card"
                }

    def _winner(self) -> dict:
        winner = defaultdict(str)
        for player in self.player_order.values():
            player = player["player"]
            
            if "name" in winner and "hand" in winner:
                previous_hand_value, previous_hand_frequency = winner["hand"]
                current_hand_value, current_hand_frequency = player.best_hand["best_hand"]

                # three of a kind
                if current_hand_frequency == 3 and previous_hand_frequency != 3:
                    winner["name"] = player.name
                    winner["hand"] = player.best_hand["best_hand"]
                    winner["short"] = player.best_hand["short"]
                    continue

                if current_hand_frequency == 3 and previous_hand_frequency == 3:
                    if current_hand_value > previous_hand_value:
                        winner["name"] = player.name
                        winner["hand"] = player.best_hand["best_hand"]
                        winner["short"] = player.best_hand["short"]
                    continue

                if current_hand_frequency != 3 and previous_hand_frequency == 3:
                    continue

                # two pair
                if isinstance(winner["hand"], list) and isinstance(player.best_hand["best_hand"], list):
                    previous_hand = sorted([pair[0] for pair in winner["hand"]])
                    current_hand = sorted([pair[0] for pair in player.best_hand["best_hand"]])

                    previous_hand = sorted([pair[0] for pair in winner["hand"]])
                    current_hand = sorted([pair[0] for pair in player.best_hand["best_hand"]])
                    greater_count = 0
                    equal_count = 0
                    for current, previous in list(zip(current_hand, previous_hand)):
                        if current > previous:
                            greater_count += 1
                        if current == previous:
                            equal_count += 1
                    if greater_count == 2 or (greater_count == 1 and equal_count == 1):
                        winner["name"] = player.name
                        winner["hand"] = player.best_hand["best_hand"]
                        winner["short"] = player.best_hand["short"]
                    continue

                if isinstance(winner["hand"], list) and not isinstance(player.best_hand["best_hand"], list):
                    continue

                if not isinstance(winner["hand"], list) and isinstance(player.best_hand["best_hand"], list):
                    winner["name"] = player.name
                    winner["hand"] = player.best_hand["best_hand"]
                    winner["short"] = player.best_hand["short"]
                    continue

                # pair
                if current_hand_frequency == 2 and previous_hand_frequency != 2:
                    winner["name"] = player.name
                    winner["hand"] = player.best_hand["best_hand"]
                    winner["short"] = player.best_hand["short"]
                    continue

                if current_hand_frequency == 2 and previous_hand_frequency == 2:
                    if current_hand_value > previous_hand_value:
                        winner["name"] = player.name
                        winner["hand"] = player.best_hand["best_hand"]
                        winner["short"] = player.best_hand["short"]
                    continue

                # high card
                if current_hand_frequency == 1 and previous_hand_frequency == 1:
                    if current_hand_value > previous_hand_value:
                        winner["name"] = player.name
                        winner["hand"] = player.best_hand["best_hand"]
                        winner["short"] = player.best_hand["short"]
                    continue               

            else:
                winner["name"] = player.name
                winner["hand"] = player.best_hand["best_hand"]
                winner["short"] = player.best_hand["short"]

        return winner
    
    def _tie(self, winner: dict) -> dict:
        for i, player in enumerate(self.player_order.values(), start=1):
            player = player["player"]
            if player.name != winner["name"]:

                if player.best_hand["best_hand"] == winner["hand"]:
                    winner[f"name_{i}"] = player.name
                    winner[f"hand_{i}"] = player.best_hand["best_hand"]
                    continue

                if player.best_hand["short"] == "Two Pair" and winner["short"] == "Two Pair":
                    player_first_pair, player_second_pair = player.best_hand["best_hand"]
                    player_first_pair_value = player_first_pair[0]
                    player_second_pair_value = player_second_pair[0]

                    winner_first_pair, winner_second_pair = winner["hand"]
                    winner_first_pair_value = winner_first_pair[0]
                    winner_second_pair_value = winner_second_pair[0]

                    if (player_first_pair_value > winner_first_pair_value and player_second_pair_value < winner_second_pair_value) or (player_first_pair_value < winner_first_pair_value and player_second_pair_value > winner_second_pair_value):
                        winner[f"name_{i}"] = player.name
                        winner[f"hand_{i}"] = player.best_hand["best_hand"]
        return winner
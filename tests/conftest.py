from collections import Counter

import pytest

from poker.utils.card import Card
from poker.utils.deck import Deck
from poker.utils.chip import PlayerStack, GameStack
from poker.utils.action import Action
from poker.utils.player import Player, Computer, Dealer
from poker.utils.constants import Cash
from poker.utils.message import GameMessage
from poker.utils.game import Game


@pytest.fixture
def card_number():
    return Card("hearts", "10")

@pytest.fixture
def card_face():
    return Card("hearts", "K")

@pytest.fixture
def deck():
    return Deck()

@pytest.fixture
def player_stack():
    return PlayerStack()

@pytest.fixture
def game_stack():
    return GameStack()

@pytest.fixture
def cash():
    return Cash

@pytest.fixture
def thirty_chips(player_stack, cash):
    player_stack.increment(cash.FIVE.value)
    player_stack.increment(cash.FIVE.value)
    player_stack.increment(cash.TWENTY.value)

@pytest.fixture
def fifty_chips(player_stack, cash):
    player_stack.increment(cash.TEN.value)
    player_stack.increment(cash.FIFTEEN.value)
    player_stack.increment(cash.TWENTY.value)
    player_stack.increment(cash.FIVE.value)

@pytest.fixture
def player(card_number, card_face):
    player = Player(name="Mills", cash=50)
    player.buy_chips(player.cash)
    player.pocket_cards.append(card_number)
    player.pocket_cards.append(card_face)
    return player

@pytest.fixture
def action(game_stack, player):
    return Action(game_stack=game_stack, player=player)

@pytest.fixture
def player_two(card_number, card_face):
    player = Player(name="Tim", cash=100)
    player.pocket_cards.append(card_number)
    player.pocket_cards.append(card_face)
    return player

@pytest.fixture
def computer(card_number, card_face):
    computer = Computer(name="Andrea", cash=50)
    computer.pocket_cards.append(card_number)
    computer.pocket_cards.append(card_face)
    return computer

@pytest.fixture
def dealer():
    return Dealer()

@pytest.fixture
def play_prompt():
    return "Welcome to Texas hold'em! Would you like to play a game? [yes/no] "

@pytest.fixture
def starting_cash_prompt():
    return "How much money would you like to start off with? "

@pytest.fixture
def competition_count_prompt():
    return "How many players would you like to play against? "

@pytest.fixture
def action_raise_prompt():
    return "The bet was raised by 10, what would you like to do? "

@pytest.fixture
def action_prompt():
    return "What would you like to do? "

@pytest.fixture
def game():
    message = GameMessage()
    dealer = Dealer()
    player = Player()
    game = Game(message=message, dealer=dealer, player=player)
    return game

@pytest.fixture
def hand_three_kind():
    suit = ["H", "D", "S", "C", "H"]
    rank = [7, 7, 7, 2, 3]
    cards = list(zip(suit, rank))
    hand = [Card(suit=card[0], rank=card[1]) for card in cards]
    return hand

@pytest.fixture
def hand_three_kind_subsequent_gt():
    suit = ["C", "H", "D", "S", "S"]
    rank = [10, 10, 10, 2, 3]
    cards = list(zip(suit, rank))
    hand = [Card(suit=card[0], rank=card[1]) for card in cards]
    return hand

@pytest.fixture
def hand_three_kind_subsequent_lt():
    suit = ["C", "D", "H", "S", "S"]
    rank = [5, 5, 5, 10, 2]
    cards = list(zip(suit, rank))
    hand = [Card(suit=card[0], rank=card[1]) for card in cards]
    return hand

@pytest.fixture
def counter_hand_three_kind(hand_three_kind):
    counter = Counter()
    for card in hand_three_kind:
        counter.update([card.rank])
    return counter

@pytest.fixture
def counter_hand_three_kind_subsequent_gt(hand_three_kind_subsequent_gt):
    counter = Counter()
    for card in hand_three_kind_subsequent_gt:
        counter.update([card.rank])
    return counter

@pytest.fixture
def counter_hand_three_kind_subsequent_lt(hand_three_kind_subsequent_lt):
    counter = Counter()
    for card in hand_three_kind_subsequent_lt:
        counter.update([card.rank])
    return counter

@pytest.fixture
def hand_rankings():
    return {
        "three_kind": False,
        "two_pair": False,
        "pair": False,
    }

@pytest.fixture
def initial_three_kind(game, hand_three_kind, counter_hand_three_kind, hand_rankings):
    person = game.player
    game._three_kind(
        hand=hand_three_kind,
        counter_hand=counter_hand_three_kind,
        person=person,
        hand_rankings=hand_rankings
    )
    return game.player, hand_rankings

@pytest.fixture
def hand_pair():
    suit = ["H", "D", "S", "C", "H"]
    rank = [7, 7, 5, 2, 3]
    cards = list(zip(suit, rank))
    hand = [Card(suit=card[0], rank=card[1]) for card in cards]
    return hand

@pytest.fixture
def hand_pair_subsequent_gt():
    suit = ["C", "H", "D", "S", "S"]
    rank = [10, 10, 8, 2, 3]
    cards = list(zip(suit, rank))
    hand = [Card(suit=card[0], rank=card[1]) for card in cards]
    return hand

@pytest.fixture
def hand_pair_subsequent_lt():
    suit = ["C", "D", "H", "S", "S"]
    rank = [5, 5, 4, 10, 2]
    cards = list(zip(suit, rank))
    hand = [Card(suit=card[0], rank=card[1]) for card in cards]
    return hand

@pytest.fixture
def counter_hand_pair(hand_pair):
    counter = Counter()
    for card in hand_pair:
        counter.update([card.rank])
    return counter

@pytest.fixture
def counter_hand_pair_subsequent_gt(hand_pair_subsequent_gt):
    counter = Counter()
    for card in hand_pair_subsequent_gt:
        counter.update([card.rank])
    return counter

@pytest.fixture
def counter_hand_pair_subsequent_lt(hand_pair_subsequent_lt):
    counter = Counter()
    for card in hand_pair_subsequent_lt:
        counter.update([card.rank])
    return counter

@pytest.fixture
def initial_pair(game, hand_pair, counter_hand_pair, hand_rankings):
    person = game.player
    game._pair(
        hand=hand_pair,
        counter_hand=counter_hand_pair,
        person=person,
        hand_rankings=hand_rankings
    )
    return game.player, hand_rankings

@pytest.fixture
def hand_high_card():
    suit = ["H", "D", "S", "C", "H"]
    rank = [9, 7, 5, 2, 3]
    cards = list(zip(suit, rank))
    hand = [Card(suit=card[0], rank=card[1]) for card in cards]
    return hand

@pytest.fixture
def hand_high_card_subsequent_gt():
    suit = ["C", "H", "D", "S", "S"]
    rank = [10, 4, 8, 2, 3]
    cards = list(zip(suit, rank))
    hand = [Card(suit=card[0], rank=card[1]) for card in cards]
    return hand

@pytest.fixture
def hand_high_card_subsequent_lt():
    suit = ["C", "D", "H", "S", "S"]
    rank = [5, 6, 4, 3, 2]
    cards = list(zip(suit, rank))
    hand = [Card(suit=card[0], rank=card[1]) for card in cards]
    return hand

@pytest.fixture
def counter_hand_high_card(hand_high_card):
    counter = Counter()
    for card in hand_high_card:
        counter.update([card.rank])
    return counter

@pytest.fixture
def counter_hand_high_card_subsequent_gt(hand_high_card_subsequent_gt):
    counter = Counter()
    for card in hand_high_card_subsequent_gt:
        counter.update([card.rank])
    return counter

@pytest.fixture
def counter_hand_high_card_subsequent_lt(hand_high_card_subsequent_lt):
    counter = Counter()
    for card in hand_high_card_subsequent_lt:
        counter.update([card.rank])
    return counter

@pytest.fixture
def initial_high_card(game, hand_high_card, counter_hand_high_card, hand_rankings):
    person = game.player
    game._pair(
        hand=hand_high_card,
        counter_hand=counter_hand_high_card,
        person=person,
        hand_rankings=hand_rankings
    )
    return game.player, hand_rankings

@pytest.fixture
def hand_two_pair():
    suit = ["H", "D", "S", "C", "H"]
    rank = [4, 4, 5, 2, 2]
    cards = list(zip(suit, rank))
    hand = [Card(suit=card[0], rank=card[1]) for card in cards]
    return hand

@pytest.fixture
def hand_two_pair_subsequent_gt():
    suit = ["C", "H", "D", "S", "S"]
    rank = [5, 5, 8, 3, 3]
    cards = list(zip(suit, rank))
    hand = [Card(suit=card[0], rank=card[1]) for card in cards]
    return hand

@pytest.fixture
def hand_two_pair_subsequent_ge():
    suit = ["C", "H", "D", "S", "S"]
    rank = [6, 6, 8, 2, 2]
    cards = list(zip(suit, rank))
    hand = [Card(suit=card[0], rank=card[1]) for card in cards]
    return hand

@pytest.fixture
def hand_two_pair_subsequent_lt():
    suit = ["C", "D", "H", "S", "S"]
    rank = [3, 3, 8, 2, 2]
    cards = list(zip(suit, rank))
    hand = [Card(suit=card[0], rank=card[1]) for card in cards]
    return hand

@pytest.fixture
def counter_hand_two_pair(hand_two_pair):
    counter = Counter()
    for card in hand_two_pair:
        counter.update([card.rank])
    return counter

@pytest.fixture
def counter_hand_two_pair_subsequent_gt(hand_two_pair_subsequent_gt):
    counter = Counter()
    for card in hand_two_pair_subsequent_gt:
        counter.update([card.rank])
    return counter

@pytest.fixture
def counter_hand_two_pair_subsequent_ge(hand_two_pair_subsequent_ge):
    counter = Counter()
    for card in hand_two_pair_subsequent_ge:
        counter.update([card.rank])
    return counter

@pytest.fixture
def counter_hand_two_pair_subsequent_lt(hand_two_pair_subsequent_lt):
    counter = Counter()
    for card in hand_two_pair_subsequent_lt:
        counter.update([card.rank])
    return counter

@pytest.fixture
def initial_two_pair(game, hand_two_pair, counter_hand_two_pair, hand_rankings):
    person = game.player
    game._two_pair(
        hand=hand_two_pair,
        counter_hand=counter_hand_two_pair,
        person=person,
        hand_rankings=hand_rankings
    )
    return game.player, hand_rankings

@pytest.fixture
def winner_setup():
    player = Player(name="Joe", cash=100)
    computer_one = Computer(name="Becca", cash=100)
    computer_two = Computer(name="Matt", cash=100)
    return player, computer_one, computer_two
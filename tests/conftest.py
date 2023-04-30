import pytest

from poker.utils.card import Card
from poker.utils.deck import Deck
from poker.utils.chip import PlayerStack, GameStack
from poker.utils.action import Action
from poker.utils.player import Player, Computer, Dealer
from poker.utils.constants import Cash


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
    player.hand.append(card_number)
    player.hand.append(card_face)
    return player

@pytest.fixture
def action(game_stack, player):
    return Action(game_stack=game_stack, player=player)

@pytest.fixture
def player_two(card_number, card_face):
    player = Player(name="Tim", cash=100)
    player.hand.append(card_number)
    player.hand.append(card_face)
    return player

@pytest.fixture
def computer(card_number, card_face):
    computer = Computer(name="Andrea", cash=50)
    computer.hand.append(card_number)
    computer.hand.append(card_face)
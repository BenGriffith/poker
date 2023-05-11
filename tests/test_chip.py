import pytest

from poker.utils.exception import IncrementException, CashException


def test_increment_exception(player_stack):
    with pytest.raises(IncrementException):
        player_stack.increment(125)


def test_cash_exception(player_stack):
    with pytest.raises(CashException):
        player_stack.increment(4)


def test_stack_increment_five(player_stack, cash):
    player_stack.increment(cash.FIVE.value)
    assert player_stack.chips[player_stack.white["name"]] == 5


def test_stack_increment_ten(player_stack, cash):
    player_stack.increment(cash.TEN.value)
    assert player_stack.chips[player_stack.white["name"]] == 10


def test_stack_increment_fifteen(player_stack, cash):
    player_stack.increment(cash.FIFTEEN.value)
    assert player_stack.chips[player_stack.white["name"]] == 15


def test_stack_increment_twenty(player_stack, cash):
    player_stack.increment(cash.TWENTY.value)
    assert player_stack.chips[player_stack.white["name"]] == 20


def test_stack_decrement(player_stack, cash):
    player_stack.increment(cash.FIVE.value)
    player_stack.increment(cash.TWENTY.value)
    
    player_stack.decrement(player_stack.white["name"], 3)
    assert player_stack.chips[player_stack.white["name"]] == 22


def test_cash_equivalent(fifty_chips, player_stack):
    fifty_chips
    assert player_stack.chips[player_stack.white["name"]] == 50
    assert player_stack.cash_equivalent() == 50


def test_game_stack_increment(game_stack):
    game_stack.increment(game_stack.white["name"], 100)
    assert game_stack.chips[game_stack.white["name"]] == 100


def test_stack_class_constants(player_stack):
    assert player_stack.white == {"name": "White", "value": 1}
    assert player_stack.red == {"name": "Red", "value": 5}
    assert player_stack.blue == {"name": "Blue", "value": 10}
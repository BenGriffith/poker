import pytest

from poker.utils.exception import IncrementException, CashException


def test_increment_exception(player_stack):
    #stack.increment(25)
    with pytest.raises(IncrementException):
        player_stack.increment(25)


def test_cash_exception(player_stack):
    with pytest.raises(CashException):
        player_stack.increment(4)


def test_stack_increment_five(player_stack, chip, cash):
    player_stack.increment(cash.FIVE.value)
    assert player_stack.chips[chip.WHITE.name] == 5


def test_stack_increment_ten(player_stack, chip, cash):
    player_stack.increment(cash.TEN.value)
    assert player_stack.chips[chip.WHITE.name] == 5
    assert player_stack.chips[chip.RED.name] == 1


def test_stack_increment_fifteen(player_stack, chip, cash):
    player_stack.increment(cash.FIFTEEN.value)
    assert player_stack.chips[chip.RED.name] == 1
    assert player_stack.chips[chip.BLUE.name] == 1


def test_stack_increment_twenty(player_stack, chip, cash):
    player_stack.increment(cash.TWENTY.value)
    assert player_stack.chips[chip.RED.name] == 2
    assert player_stack.chips[chip.BLUE.name] == 1


def test_stack_decrement(player_stack, chip, cash):
    player_stack.increment(cash.FIVE.value)
    player_stack.increment(cash.TWENTY.value)
    
    player_stack.decrement(chip.WHITE.name, 3)
    assert player_stack.chips[chip.WHITE.name] == 2

    player_stack.decrement(chip.RED.name, 1)
    player_stack.decrement(chip.BLUE.name, 1)
    assert player_stack.chips[chip.RED.name] == 1
    assert player_stack.chips[chip.BLUE.name] == 0


def test_chip_count(player_stack, cash):
    player_stack.increment(cash.FIVE.value)
    player_stack.increment(cash.FIVE.value)
    player_stack.increment(cash.TWENTY.value)
    assert player_stack.chip_count() == (10, 2, 1) # WHITE: 10, RED: 2, BLUE: 1


def test_cash_equivalent(player_stack, chip, cash):
    player_stack.increment(cash.TEN.value)
    player_stack.increment(cash.FIFTEEN.value)
    player_stack.increment(cash.TWENTY.value)
    player_stack.increment(cash.FIVE.value)

    assert player_stack.chips[chip.WHITE.name] == 10
    assert player_stack.chips[chip.RED.name] == 4
    assert player_stack.chips[chip.BLUE.name] == 2

    assert player_stack.cash_equivalent() == 50


def test_game_stack_increment(game_stack, chip, cash):
    game_stack.increment(chip.WHITE.value, 5)
    game_stack.increment(chip.RED.value, 2)
    assert game_stack.chips[chip.WHITE.value] == 5
    assert game_stack.chips[chip.RED.value] == 2
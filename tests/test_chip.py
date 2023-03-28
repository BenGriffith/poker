import pytest

from poker.utils.exception import IncrementException, CashException


def test_increment_exception(stack):
    #stack.increment(25)
    with pytest.raises(IncrementException):
        stack.increment(25)


def test_cash_exception(stack):
    with pytest.raises(CashException):
        stack.increment(4)


def test_stack_increment_five(stack, chip, cash):
    stack.increment(cash.FIVE.value)
    assert stack.chips[chip.WHITE.name] == 5


def test_stack_increment_ten(stack, chip, cash):
    stack.increment(cash.TEN.value)
    assert stack.chips[chip.WHITE.name] == 5
    assert stack.chips[chip.RED.name] == 1


def test_stack_increment_fifteen(stack, chip, cash):
    stack.increment(cash.FIFTEEN.value)
    assert stack.chips[chip.RED.name] == 1
    assert stack.chips[chip.BLUE.name] == 1


def test_stack_increment_twenty(stack, chip, cash):
    stack.increment(cash.TWENTY.value)
    assert stack.chips[chip.RED.name] == 2
    assert stack.chips[chip.BLUE.name] == 1


def test_stack_decrement(stack, chip, cash):
    stack.increment(cash.FIVE.value)
    stack.increment(cash.TWENTY.value)
    
    stack.decrement(chip.WHITE.name, 3)
    assert stack.chips[chip.WHITE.name] == 2

    stack.decrement(chip.RED.name, 1)
    stack.decrement(chip.BLUE.name, 1)
    assert stack.chips[chip.RED.name] == 1
    assert stack.chips[chip.BLUE.name] == 0


def test_chip_count(stack, cash):
    stack.increment(cash.FIVE.value)
    stack.increment(cash.FIVE.value)
    stack.increment(cash.TWENTY.value)
    assert stack.chip_count() == (10, 2, 1) # WHITE: 10, RED: 2, BLUE: 1


def test_cash_equivalent(stack, chip, cash):
    stack.increment(cash.TEN.value)
    stack.increment(cash.FIFTEEN.value)
    stack.increment(cash.TWENTY.value)
    stack.increment(cash.FIVE.value)

    assert stack.chips[chip.WHITE.name] == 10
    assert stack.chips[chip.RED.name] == 4
    assert stack.chips[chip.BLUE.name] == 2

    assert stack.cash_equivalent() == 50
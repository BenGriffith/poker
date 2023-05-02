import pytest

from poker.utils.message import GameMessage
from poker.utils.action import Action
from poker.utils.constants import COMPETITION
from poker.utils.exception import CashException, RangeException, InvalidActionException, NegativeException, GamePlayException, NotReadyException

message = GameMessage()


@pytest.mark.parametrize("test_input, expected", [
    ("yes", message.decision),
    ("y", message.decision),
    ("no", message.decision),
    ("n", message.decision),
    ("YES", message.decision),
    ("Y", message.decision),
    ("NO", message.decision),
    ("N", message.decision),
])
def test_play_valid_response(monkeypatch, play_prompt, test_input, expected):
    monkeypatch.setattr("builtins.input", lambda _: test_input)
    response = input(play_prompt).lower()
    assert response in expected


@pytest.mark.parametrize("test_input, expected", [
    ("yeah", message.decision),
    ("sure", message.decision),
    ("OK", message.decision),
])
def test_play_invalid_response(monkeypatch, play_prompt, test_input, expected):
    monkeypatch.setattr("builtins.input", lambda _: test_input)
    response = input(play_prompt).lower()
    assert response not in expected


@pytest.mark.parametrize("test_input, expected", [
    ("5", message.cash_options),
    ("10", message.cash_options),
    ("15", message.cash_options),
    ("20", message.cash_options),
    ("50", message.cash_options),
    ("100", message.cash_options),
])
def test_starting_cash_valid_response(monkeypatch, starting_cash_prompt, test_input, expected):
    monkeypatch.setattr("builtins.input", lambda _: test_input)
    response = int(input(starting_cash_prompt))
    assert response in expected


@pytest.mark.parametrize("test_input, expected", [
    ("6", message.cash_options),
    ("22", message.cash_options),
    ("ten", message.cash_options),
    ("1000", message.cash_options),
    ("five", message.cash_options),
])
def test_starting_cash_invalid_response(monkeypatch, starting_cash_prompt,
                                        test_input, expected):
    with pytest.raises((CashException, ValueError)):
        monkeypatch.setattr("builtins.input", lambda _: test_input)
        response = int(input(starting_cash_prompt))
        if response not in expected:
            raise CashException
        

@pytest.mark.parametrize("test_input, expected", [
    ("1", COMPETITION),
    ("2", COMPETITION),
    ("3", COMPETITION),
    ("4", COMPETITION),
])
def test_competition_count_valid_response(monkeypatch, competition_count_prompt,
                                          test_input, expected):
    monkeypatch.setattr("builtins.input", lambda _: test_input)
    response = int(input(competition_count_prompt))
    assert response in expected
    

@pytest.mark.parametrize("test_input, expected", [
    ("one", COMPETITION),
    ("5", COMPETITION),
    ("6", COMPETITION),
    ("two", COMPETITION),
])
def test_competition_count_invalid_response(monkeypatch, competition_count_prompt,
                                          test_input, expected):
    with pytest.raises((ValueError, RangeException)):
        monkeypatch.setattr("builtins.input", lambda _: test_input)
        response = int(input(competition_count_prompt))
        if response not in expected:
            raise RangeException
        

@pytest.mark.parametrize("test_input, expected", [
    ("CALL", [Action.CALL, Action.FOLD]),
    ("call", [Action.CALL, Action.FOLD]),
    ("FOLD", [Action.CALL, Action.FOLD]),
    ("fold", [Action.CALL, Action.FOLD])
])
def test_action_valid_response_raise(monkeypatch, action_raise_prompt, test_input, expected):
    monkeypatch.setattr("builtins.input", lambda _: test_input)
    response = input(action_raise_prompt).lower()
    assert response in expected


@pytest.mark.parametrize("test_input, expected", [
    ("CHECK", [Action.CHECK, Action.RAISE, Action.FOLD]),
    ("check", [Action.CHECK, Action.RAISE, Action.FOLD]),
    ("RAISE", [Action.CHECK, Action.RAISE, Action.FOLD]),
    ("raise", [Action.CHECK, Action.RAISE, Action.FOLD]),
    ("FOLD", [Action.CHECK, Action.RAISE, Action.FOLD]),
    ("fold", [Action.CHECK, Action.RAISE, Action.FOLD]),
])
def test_action_valid_response_no_raise(monkeypatch, action_prompt, test_input, expected):
    monkeypatch.setattr("builtins.input", lambda _: test_input)
    response = input(action_prompt).lower()
    assert response in expected   


@pytest.mark.parametrize("test_input, expected", [
    ("ten", [Action.CALL, Action.FOLD]),
    ("raise", [Action.CALL, Action.FOLD]),
    ("check", [Action.CALL, Action.FOLD]),
    ("5", [Action.CALL, Action.FOLD]),
])
def test_action_invalid_response_raise(monkeypatch, action_raise_prompt, test_input, expected):
    with pytest.raises((ValueError, InvalidActionException)):
        monkeypatch.setattr("builtins.input", lambda _: test_input)
        response = input(action_raise_prompt).lower()
        if response not in expected:
            raise InvalidActionException


@pytest.mark.parametrize("test_input, expected", [
    ("call", [Action.CHECK, Action.RAISE, Action.FOLD]),
    ("CALL", [Action.CHECK, Action.RAISE, Action.FOLD]),
    ("ten", [Action.CHECK, Action.RAISE, Action.FOLD])
])
def test_action_invalid_response(monkeypatch, action_prompt, test_input, expected):
    with pytest.raises((ValueError, InvalidActionException)):
        monkeypatch.setattr("builtins.input", lambda _: test_input)
        response = input(action_prompt).lower()
        if response not in expected:
            raise InvalidActionException
        

@pytest.mark.parametrize("test_input, expected", [
    ("1", 1),
    ("5", 5),
    ("20", 20),
    ("76", 76),
])
def test_increase_valid_response(monkeypatch, test_input, expected):
    monkeypatch.setattr("builtins.input", lambda _: test_input)
    response = int(input("how much would you like to raise? "))
    assert response == expected


@pytest.mark.parametrize("test_input", ["one", "-10", "ten", "0"])
def test_increase_invalid_response(monkeypatch, test_input):
    with pytest.raises((ValueError, NegativeException)):
        monkeypatch.setattr("builtins.input", lambda _: test_input)
        response = int(input("How much would you like to raise? "))
        if response <= 0:
            raise NegativeException
        

@pytest.mark.parametrize("test_input, expected", [
    ("yes", message.decision),
    ("y", message.decision),
    ("YES", message.decision),
    ("Y", message.decision),
])
def test_game_progression_prompt_valid_response(monkeypatch, test_input, expected):
    monkeypatch.setattr("builtins.input", lambda _: test_input)
    response = input("Are you ready to continue? [yes/no] ").lower()
    assert response in expected


@pytest.mark.parametrize("test_input, expected", [
    ("yeah", message.decision),
    ("ok", message.decision),
    ("sure", message.decision),
    ("no", ["no", "n"]),
    ("n", ["no", "n"])
])
def test_game_progression_prompt_invalid_response(monkeypatch, test_input, expected):
    with pytest.raises((GamePlayException, NotReadyException)):
        monkeypatch.setattr("builtins.input", lambda _: test_input)
        response = input("Are you ready to continue? [yes/no] ").lower()
        if response not in expected:
            raise GamePlayException
        if response in expected:
            raise NotReadyException
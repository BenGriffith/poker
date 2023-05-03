from poker.utils.chip import GameStack
from poker.utils.player import Player


def test_action_class_constants(action):
    assert action.CHECK == "check"
    assert action.RAISE == "raise"
    assert action.CALL == "call"
    assert action.FOLD == "fold"


def test_action(action):
    assert isinstance(action.game_stack, GameStack)
    assert isinstance(action.person, Player)
    assert action.person.name == "Mills"
    assert action.person.cash == 0
    assert action.person.stack.chips == {"White": 50}
    assert len(action.person.pocket_cards) == 2


def test_bet(action):
    action.bet(chip="White", value=10)
    assert action.game_stack.chips == {"White": 10}
    assert action.person.stack.chips == {"White": 40}


def test_fold(action):
    action.fold()
    assert action.person.pocket_cards == []


def test_blind(action):
    action.blind(chip="White", value=1) # small blind
    assert action.game_stack.chips == {"White": 1}
    assert action.person.stack.chips == {"White": 49}

    action.blind(chip="White", value=2) # big blind
    assert action.game_stack.chips == {"White": 3}
    assert action.person.stack.chips == {"White": 47}


def test_call(action):
    action.call(chip="White", value=10)
    assert action.game_stack.chips == {"White": 10}
    assert action.person.stack.chips == {"White": 40}


def test_raise(action):
    action.increase(chip="White", value=20)
    assert action.game_stack.chips == {"White": 20}
    assert action.person.stack.chips == {"White": 30}
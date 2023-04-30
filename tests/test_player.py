def test_player(player_two):
    assert player_two.PLAYER == "Player"
    assert player_two.COMPUTER == "Computer"
    assert player_two.name == "Tim"
    assert player_two.cash == 100
    assert len(player_two.hand) == 2
    assert player_two.kind == "Player"


def test_player_buy_chips(player_two):
    player_two.buy_chips(value=20)
    assert player_two.stack.chips == {"White": 20}
    assert player_two.cash == 80


def test_player_process_bet(player_two):
    player_two.buy_chips(value=100)
    player_two.process_bet(raise_amount=20)
    assert player_two.stack.chips == {"White": 80}


def test_computer_select_action(computer):
    pass
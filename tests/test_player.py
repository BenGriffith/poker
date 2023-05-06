def test_player(player_two):
    assert player_two.name == "Tim"
    assert player_two.cash == 100
    assert len(player_two.pocket_cards) == 2
    assert player_two.kind == "Player"


def test_player_buy_chips(player_two):
    player_two.buy_chips(value=20)
    assert player_two.stack.chips == {"White": 20}
    assert player_two.cash == 80


def test_player_process_bet(player_two):
    player_two.buy_chips(value=100)
    player_two.process_bet(raise_amount=20)
    assert player_two.stack.chips == {"White": 80}


def test_computer_select_random_action(computer):
    action = computer.select_action(raise_amount=0) 
    assert action in ["check", "raise"]


def test_computer_select_call(computer):
    computer.buy_chips(value=20)
    assert computer.select_action(raise_amount=10) == "call"


def test_computer_select_fold(computer):
    computer.buy_chips(value=20)
    assert computer.select_action(raise_amount=30) == "fold"


def test_computer_process_random_bet(computer):
    computer.buy_chips(value=20)
    assert computer.stack.chips == {"White": 20}
    white_chips_one_third = computer.stack.chips["White"] // 3
    assert computer.process_bet(raise_amount=0) <= white_chips_one_third


def test_computer_process_call(computer):
    computer.buy_chips(value=20)
    assert computer.cash == 30
    assert computer.stack.chips == {"White": 20}
    computer.process_bet(raise_amount=10) # call
    assert computer.stack.chips == {"White": 10}


def test_dealer_shuffle_deck(dealer):
    unshuffled_first_card = dealer.deck.cards[0]
    dealer.shuffle_deck()
    shuffled_first_card= dealer.deck.cards[0]
    assert unshuffled_first_card != shuffled_first_card


def test_dealer_deal_card(dealer, player):
    last_card_suit = dealer.deck.cards[-1].suit
    last_card_rank = dealer.deck.cards[-1].rank
    assert len(player.pocket_cards) == 2
    dealer.deal_card(person=player)
    assert len(player.pocket_cards) == 3
    player_last_card_suit = player.pocket_cards[-1].suit
    player_last_card_rank = player.pocket_cards[-1].rank
    assert last_card_suit == player_last_card_suit
    assert last_card_rank == player_last_card_rank
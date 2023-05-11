def test_convert_hand_to_counter(game, hand_three_kind, counter_hand_three_kind):
    hand_to_counter = game._convert_hand_to_counter(hand_three_kind)
    assert hand_to_counter == counter_hand_three_kind


def test_initial_three_kind(game, hand_three_kind, counter_hand_three_kind, hand_rankings):
    person = game.player
    game._three_kind(
        hand=hand_three_kind,
        counter_hand=counter_hand_three_kind,
        person=person,
        hand_rankings=hand_rankings
    )
    assert game.player.best_hand == {
        "hand": hand_three_kind,
        "counter_hand": counter_hand_three_kind,
        "best_hand": counter_hand_three_kind.most_common()[0],
        "short": "Three of a Kind"
    }
    assert counter_hand_three_kind.most_common()[0] == (7,3)
    assert hand_rankings["three_kind"] == True


def test_subsequent_three_kind_gt(initial_three_kind, game, hand_three_kind_subsequent_gt, counter_hand_three_kind_subsequent_gt):
    person, hand_rankings = initial_three_kind
    assert person.best_hand["best_hand"] == (7,3)
    game._three_kind(
        hand=hand_three_kind_subsequent_gt,
        counter_hand=counter_hand_three_kind_subsequent_gt,
        person=person,
        hand_rankings=hand_rankings
    )
    assert game.player.best_hand == {
        "hand": hand_three_kind_subsequent_gt,
        "counter_hand": counter_hand_three_kind_subsequent_gt,
        "best_hand": counter_hand_three_kind_subsequent_gt.most_common()[0],
        "short": "Three of a Kind"
    }
    assert counter_hand_three_kind_subsequent_gt.most_common()[0] == (10,3)


def test_subsequent_three_kind_lt(initial_three_kind, game, hand_three_kind_subsequent_lt, counter_hand_three_kind_subsequent_lt):
    person, hand_rankings = initial_three_kind
    assert person.best_hand["best_hand"] == (7,3)
    game._three_kind(
        hand=hand_three_kind_subsequent_lt,
        counter_hand=counter_hand_three_kind_subsequent_lt,
        person=person,
        hand_rankings=hand_rankings
    )
    assert person.best_hand["best_hand"] == (7,3)


def test_initial_pair(game, hand_pair, counter_hand_pair, hand_rankings):
    person = game.player
    game._pair(
        hand=hand_pair,
        counter_hand=counter_hand_pair,
        person=person,
        hand_rankings=hand_rankings
    )
    assert game.player.best_hand == {
        "hand": hand_pair,
        "counter_hand": counter_hand_pair,
        "best_hand": counter_hand_pair.most_common()[0],
        "short": "Pair"
    }
    assert counter_hand_pair.most_common()[0][0] == 7
    assert hand_rankings["pair"] == True


def test_subsequent_pair_gt(initial_pair, game, hand_pair_subsequent_gt, counter_hand_pair_subsequent_gt):
    person, hand_rankings = initial_pair
    assert person.best_hand["best_hand"] == (7,2)
    game._pair(
        hand=hand_pair_subsequent_gt,
        counter_hand=counter_hand_pair_subsequent_gt,
        person=person,
        hand_rankings=hand_rankings
    )
    assert game.player.best_hand == {
        "hand": hand_pair_subsequent_gt,
        "counter_hand": counter_hand_pair_subsequent_gt,
        "best_hand": counter_hand_pair_subsequent_gt.most_common()[0],
        "short": "Pair"
    }
    assert counter_hand_pair_subsequent_gt.most_common()[0] == (10,2)


def test_subsequent_pair_lt(initial_pair, game, hand_pair_subsequent_lt, counter_hand_pair_subsequent_lt):
    person, hand_rankings = initial_pair
    assert person.best_hand["best_hand"] == (7,2)
    game._pair(
        hand=hand_pair_subsequent_lt,
        counter_hand=counter_hand_pair_subsequent_lt,
        person=person,
        hand_rankings=hand_rankings
    )
    assert person.best_hand["best_hand"] == (7,2)


def test_initial_high_card(game, hand_high_card, counter_hand_high_card):
    person = game.player
    game._high_card(
        hand=hand_high_card,
        counter_hand=counter_hand_high_card,
        person=person
    )
    assert game.player.best_hand == {
        "hand": hand_high_card,
        "counter_hand": counter_hand_high_card,
        "best_hand": (9,1),
        "short": "High Card"
    }


def test_subsequent_high_card_gt(initial_high_card, game, hand_high_card_subsequent_gt, counter_hand_high_card_subsequent_gt):
    person, _ = initial_high_card
    game._high_card(
        hand=hand_high_card_subsequent_gt,
        counter_hand=counter_hand_high_card_subsequent_gt,
        person=person
    )
    assert game.player.best_hand == {
        "hand": hand_high_card_subsequent_gt,
        "counter_hand": counter_hand_high_card_subsequent_gt,
        "best_hand": (10,1),
        "short": "High Card"
    }


def test_subsequent_high_card_lt(initial_high_card, game, hand_high_card_subsequent_lt, counter_hand_high_card_subsequent_lt):
    person, _ = initial_high_card
    game._high_card(
        hand=hand_high_card_subsequent_lt,
        counter_hand=counter_hand_high_card_subsequent_lt,
        person=person
    )
    assert person.best_hand["best_hand"] == (9,1)


def test_initial_two_pair(game, hand_two_pair, counter_hand_two_pair, hand_rankings):
    person = game.player
    game._two_pair(
        hand=hand_two_pair,
        counter_hand=counter_hand_two_pair,
        person=person,
        hand_rankings=hand_rankings
    )
    assert game.player.best_hand == {
        "hand": hand_two_pair,
        "counter_hand": counter_hand_two_pair,
        "best_hand": [(4,2),(2,2)],
        "short": "Two Pair"
    }
    assert hand_rankings["two_pair"] == True


def test_subsequent_two_pair_gt(initial_two_pair, game, hand_two_pair_subsequent_gt, counter_hand_two_pair_subsequent_gt):
    person, hand_rankings = initial_two_pair
    assert person.best_hand["best_hand"] == [(4,2),(2,2)]
    game._two_pair(
        hand=hand_two_pair_subsequent_gt,
        counter_hand=counter_hand_two_pair_subsequent_gt,
        person=person,
        hand_rankings=hand_rankings
    )
    assert game.player.best_hand == {
        "hand": hand_two_pair_subsequent_gt,
        "counter_hand": counter_hand_two_pair_subsequent_gt,
        "best_hand": [(5,2),(3,2)],
        "short": "Two Pair"
    }


def test_subsequent_two_pair_ge(initial_two_pair, game, hand_two_pair_subsequent_ge, counter_hand_two_pair_subsequent_ge):
    person, hand_rankings = initial_two_pair
    assert person.best_hand["best_hand"] == [(4,2),(2,2)]
    game._two_pair(
        hand=hand_two_pair_subsequent_ge,
        counter_hand=counter_hand_two_pair_subsequent_ge,
        person=person,
        hand_rankings=hand_rankings
    )
    assert game.player.best_hand == {
        "hand": hand_two_pair_subsequent_ge,
        "counter_hand": counter_hand_two_pair_subsequent_ge,
        "best_hand": [(6,2),(2,2)],
        "short": "Two Pair"
    }


def test_subsequent_two_pair_lt(initial_two_pair, game, hand_two_pair_subsequent_lt, counter_hand_two_pair_subsequent_lt):
    person, hand_rankings = initial_two_pair
    assert person.best_hand["best_hand"] == [(4,2),(2,2)]
    game._two_pair(
        hand=hand_two_pair_subsequent_lt,
        counter_hand=counter_hand_two_pair_subsequent_lt,
        person=person,
        hand_rankings=hand_rankings
    )
    assert game.player.best_hand == {
        "hand": hand_two_pair_subsequent_lt,
        "counter_hand": counter_hand_two_pair_subsequent_lt,
        "best_hand": [(3,2),(2,2)],
        "short": "Two Pair"
    }


def test_winner_no_current_winner(game, winner_setup):
    player, computer_one, computer_two = winner_setup
    player.best_hand["best_hand"] = (4,2)
    player.best_hand["short"] = "Pair"
    game.player_order = {1: {"player": player}}
    assert game._winner() == {
        "name": "Joe",
        "hand": (4,2),
        "short": "Pair"
    }


def test_winner_three_kind_first_scenario(game, winner_setup):
    player, computer_one, computer_two = winner_setup
    player.best_hand["best_hand"] = (4,2)
    player.best_hand["short"] = "Pair"
    computer_one.best_hand["best_hand"] = (5,3)
    computer_one.best_hand["short"] = "Three of a Kind"
    game.player_order = {
        1: {"player": player},
        2: {"player": computer_one},
    }
    assert game._winner() == {
        "name": "Becca",
        "hand": (5,3),
        "short": "Three of a Kind"
    }


def test_winner_three_kind_second_scenario_previous_gt(game, winner_setup):
    player, computer_one, computer_two = winner_setup
    player.best_hand["best_hand"] = (6,3)
    player.best_hand["short"] = "Three of a Kind"
    computer_one.best_hand["best_hand"] = (5,3)
    computer_one.best_hand["short"] = "Three of a Kind"
    game.player_order = {
        1: {"player": player},
        2: {"player": computer_one},
    }
    assert game._winner() == {
        "name": "Joe",
        "hand": (6,3),
        "short": "Three of a Kind"
    }


def test_winner_three_kind_second_scenario_previous_lt(game, winner_setup):
    player, computer_one, computer_two = winner_setup
    player.best_hand["best_hand"] = (5,3)
    player.best_hand["short"] = "Three of a Kind"
    computer_one.best_hand["best_hand"] = (8,3)
    computer_one.best_hand["short"] = "Three of a Kind"
    game.player_order = {
        1: {"player": player},
        2: {"player": computer_one},
    }
    assert game._winner() == {
        "name": "Becca",
        "hand": (8,3),
        "short": "Three of a Kind"
    }


def test_winner_three_kind_third_scenario(game, winner_setup):
    player, computer_one, computer_two = winner_setup
    player.best_hand["best_hand"] = (10,3)
    player.best_hand["short"] = "Three of a Kind"
    computer_one.best_hand["best_hand"] = [(6,2),(4,2)]
    computer_one.best_hand["short"] = "Two Pair"
    game.player_order = {
        1: {"player": player},
        2: {"player": computer_one},
    }
    assert game._winner() == {
        "name": "Joe",
        "hand": (10,3),
        "short": "Three of a Kind"
    }


def test_winner_high_card_previous_gt(game, winner_setup):
    player, computer_one, computer_two = winner_setup
    player.best_hand["best_hand"] = (9,1)
    player.best_hand["short"] = "High Card"
    computer_one.best_hand["best_hand"] = (10,1)
    computer_one.best_hand["short"] = "High Card"
    computer_two.best_hand["best_hand"] = (8,1)
    computer_two.best_hand["short"] = "High Card"
    game.player_order = {
        1: {"player": player},
        2: {"player": computer_one},
        3: {"player": computer_two},
    }
    assert game._winner() == {
        "name": "Becca",
        "hand": (10,1),
        "short": "High Card"
    }


def test_winner_high_card_previous_lt(game, winner_setup):
    player, computer_one, computer_two = winner_setup
    player.best_hand["best_hand"] = (8,1)
    player.best_hand["short"] = "High Card"
    computer_one.best_hand["best_hand"] = (9,1)
    computer_one.best_hand["short"] = "High Card"
    computer_two.best_hand["best_hand"] = (10,1)
    computer_two.best_hand["short"] = "High Card"
    game.player_order = {
        1: {"player": player},
        2: {"player": computer_one},
        3: {"player": computer_two},
    }
    assert game._winner() == {
        "name": "Matt",
        "hand": (10,1),
        "short": "High Card"
    }


def test_winner_pair_first_scenario(game, winner_setup):
    player, computer_one, computer_two = winner_setup
    player.best_hand["best_hand"] = (8,1)
    player.best_hand["short"] = "High Card"
    computer_one.best_hand["best_hand"] = (9,1)
    computer_one.best_hand["short"] = "High Card"
    computer_two.best_hand["best_hand"] = (10,2)
    computer_two.best_hand["short"] = "Pair"
    game.player_order = {
        1: {"player": player},
        2: {"player": computer_one},
        3: {"player": computer_two},
    }
    assert game._winner() == {
        "name": "Matt",
        "hand": (10,2),
        "short": "Pair"
    }


def test_winner_pair_second_scenario_previous_gt(game, winner_setup):
    player, computer_one, computer_two = winner_setup
    player.best_hand["best_hand"] = (10,2)
    player.best_hand["short"] = "Pair"
    computer_one.best_hand["best_hand"] = (9,2)
    computer_one.best_hand["short"] = "Pair"
    computer_two.best_hand["best_hand"] = (8,1)
    computer_two.best_hand["short"] = "High Card"
    game.player_order = {
        1: {"player": player},
        2: {"player": computer_one},
        3: {"player": computer_two},
    }
    assert game._winner() == {
        "name": "Joe",
        "hand": (10,2),
        "short": "Pair"
    }

def test_winner_pair_second_scenario_current_gt(game, winner_setup):
    player, computer_one, computer_two = winner_setup
    player.best_hand["best_hand"] = (8,1)
    player.best_hand["short"] = "High Card"
    computer_one.best_hand["best_hand"] = (8,2)
    computer_one.best_hand["short"] = "Pair"
    computer_two.best_hand["best_hand"] = (9,2)
    computer_two.best_hand["short"] = "Pair"
    game.player_order = {
        1: {"player": player},
        2: {"player": computer_one},
        3: {"player": computer_two},
    }
    assert game._winner() == {
        "name": "Matt",
        "hand": (9,2),
        "short": "Pair"
    }


def test_winner_two_pair_first_scenario_previous_gt(game, winner_setup):
    player, computer_one, computer_two = winner_setup
    player.best_hand["best_hand"] = [(10,2),(9,2)]
    player.best_hand["short"] = "Two Pair"
    computer_one.best_hand["best_hand"] = [(8,2),(7,2)]
    computer_one.best_hand["short"] = "Two Pair"
    computer_two.best_hand["best_hand"] = [(6,2),(9,2)]
    computer_two.best_hand["short"] = "Two Pair"
    game.player_order = {
        1: {"player": player},
        2: {"player": computer_one},
        3: {"player": computer_two},
    }
    assert game._winner() == {
        "name": "Joe",
        "hand": [(10,2),(9,2)],
        "short": "Two Pair"
    }


def test_winner_two_pair_first_scenario_previous_lt(game, winner_setup):
    player, computer_one, computer_two = winner_setup
    player.best_hand["best_hand"] = [(2,2),(3,2)]
    player.best_hand["short"] = "Two Pair"
    computer_one.best_hand["best_hand"] = [(8,2),(7,2)]
    computer_one.best_hand["short"] = "Two Pair"
    computer_two.best_hand["best_hand"] = [(6,2),(9,2)]
    computer_two.best_hand["short"] = "Two Pair"
    game.player_order = {
        1: {"player": player},
        2: {"player": computer_one},
        3: {"player": computer_two},
    }
    assert game._winner() == {
        "name": "Becca",
        "hand": [(8,2),(7,2)],
        "short": "Two Pair"
    }


def test_winner_two_pair_first_scenario_previous_ge(game, winner_setup):
    player, computer_one, computer_two = winner_setup
    player.best_hand["best_hand"] = [(10,2),(9,2)]
    player.best_hand["short"] = "Two Pair"
    computer_one.best_hand["best_hand"] = [(8,2),(9,2)]
    computer_one.best_hand["short"] = "Two Pair"
    computer_two.best_hand["best_hand"] = [(6,2),(9,2)]
    computer_two.best_hand["short"] = "Two Pair"
    game.player_order = {
        1: {"player": player},
        2: {"player": computer_one},
        3: {"player": computer_two},
    }
    assert game._winner() == {
        "name": "Joe",
        "hand": [(10,2),(9,2)],
        "short": "Two Pair"
    }
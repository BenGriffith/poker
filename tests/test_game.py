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
    person, hand_rankings = initial_high_card
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
    person, hand_rankings = initial_high_card
    game._high_card(
        hand=hand_high_card_subsequent_lt,
        counter_hand=counter_hand_high_card_subsequent_lt,
        person=person
    )
    assert person.best_hand["best_hand"] == (9,1)
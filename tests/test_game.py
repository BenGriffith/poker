def test_convert_hand_to_counter(game, hand_three_kind, counter_hand_three_kind):
    hand_to_counter = game._convert_hand_to_counter(hand_three_kind)
    assert hand_to_counter == counter_hand_three_kind


def test_three_kind(game, hand_three_kind, counter_hand_three_kind, hand_rankings):
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
    assert hand_rankings["three_kind"] == True
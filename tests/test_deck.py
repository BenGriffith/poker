from poker.utils.card import Card

def test_card(card_number):
    assert card_number.suit == "hearts"
    assert isinstance(card_number.suit, str)
    assert card_number.rank == "10"
    assert isinstance(card_number.rank, str)


def test_card_value(card_face):
    assert card_face.value() == 13


def test_deck(deck):
    assert len(deck.cards) == 52
    assert isinstance(deck.cards[0], (Card))
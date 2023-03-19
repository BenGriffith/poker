from poker.utils.card import Card

def test_card(card):
    assert card.suit == "hearts"
    assert isinstance(card.suit, (str)) == True
    assert card.rank == "10"
    assert isinstance(card.rank, (str)) == True

def test_deck(deck):
    assert len(deck.cards) == 52
    assert isinstance(deck.cards[0], (Card)) == True
    assert deck.cards != deck.shuffle_deck()
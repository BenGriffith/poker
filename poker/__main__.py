from poker.utils.game import Game
from poker.utils.player import Player, Dealer
from poker.utils.message import GameMessage


game_message = GameMessage()
dealer = Dealer()
player = Player()
game = Game(game_message, dealer, player)
game.start()
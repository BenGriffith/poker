from poker.utils.game import GameMessage, Game
from poker.utils.player import Player, Dealer
from poker.utils.constants import Decision


game_message = GameMessage()
dealer = Dealer()
player = Player()
game = Game(game_message, dealer, player)
game.start()
print("Thanks for joining! Hope to see you again soon!")
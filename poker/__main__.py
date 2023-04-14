from poker.utils.game import GameMessage, Game, TestApp
from poker.utils.player import Player, Dealer

from textual.app import App, ComposeResult
from textual.widgets import Button, Header, Label


class PokerApp(App):
    CSS_PATH = "utils/css/main-menu.css"
    TITLE = "Welcome to Texas hold'em!"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Would you like to play a game?", id="question")
        yield Button("Yes", id="yes", variant="primary")
        yield Button("No", id="no", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.exit(event.button.id)

app = PokerApp()
reply = app.run()
if reply == "yes":
    test_app = TestApp()
    test_app.run()


# game_message = GameMessage()
# dealer = Dealer()
# player = Player()
# game = Game(game_message, dealer, player)
# game.start()
# print("Thanks for joining! Hope to see you again soon!")
## General Info
Command Line Single-player game of Texas Hold'Em poker. 

At the beginning of the game, you are asked to define how much cash each player will receive along with how many players you would like to play against. You can select from 1 to 4 players. Your competition is then randomly created and a player order is defined for the duration of the game. This order is used to control the blind and betting process.

The game consists of the following stages:
- Preflop: two pocket cards are dealt to each player and big/small blinds are processed
- Flop: discard top card from the stack and deal three community cards
- Turn: discard top card from the stack and deal one community card
- River: discard top card from the stack and deal last community card
- Showdown: player best hands are evaluated and winner is selected

After each of the above stages a round of betting takes place following the defined player order allowing players to check, call, raise or fold. If a player folds, they are simply removed from the player order and the game will continue with the remaining players. During the final stage of the game, the best hand for each player is selected, compared against other players and a winner is selected. 

Currently, logic for the following hands is supported:

- Three of a Kind
- Two Pair
- Pair
- High Card

Additionally, the game only supports use of white chips. I created issues for the remaining poker hands and chip denominations and plan to add them at a later date. While I have written and conducted a lot of testing to ensure a high quality experience, it's possible bugs do exist. Please report any you might experience and I will do my best to squash them promptly.

## Setup
```
$ pip install play-poker
$ python -m poker
```
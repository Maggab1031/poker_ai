# poker_ai

## poker.py
The module for controlling the mechanics of the virtual poker game, imports hand.py

### card
an object class that contains info like rank and suit

### deck
a collection of card objects that is in random order and will pop the top much like a stack
### player
a way to interface with the user, control the decisions, and track the amounts.
### game
a collection of players, a deck, and a way to restart rounds
### round
a way to keep track of all actions that occur in a round for easy parsing in the future.


## hand
a collection of card objects, has an intrinsic attribute of value (pair, full house, etc.)

## ai.py
Work in progress

A Python3 library that you can use to play a game of bobail. This is just a set of classes that you can use in your code, it's not an interactive shell for the game.

[![Build Status](https://travis-ci.org/jasondaming/bobail.svg?branch=master)](https://travis-ci.org/github/jasondaming/bobail)

# Assumptions

The rules used are from BoardGameAreana (http://en.doc.boardgamearena.com/Gamehelpbobail). This means an 5x5 board.

Each position on the board is numbered 1 to 25. Each move is represented as an array with two values: starting position and ending position. So if you're starting a new game, one of the available moves is `[22, 7]` for player 1.

Each turn (other than the first) will be a series of two moves.  First moving the Bobail then a player token.

# Usage

Create a new game:

```python
from bobail.game import Game

game = Game()
```

See whose turn it is:

```python
game.whose_turn() #1 or 2
```

Get the possible moves:

```python
game.get_possible_moves() #[[9, 13], [9, 14], [10, 14], [10, 15], [11, 15], [11, 16], [12, 16]]
```

Make a move:

```python
game.move([9, 13])
```

Check if the game is over:

```python
game.is_over() #True or False
```

Find out who won:

```python
game.get_winner() #None or 1 or 2
```

Review the move history:

```python
game.moves #[[int, int], [int, int], ...]
```

Review the pieces on the board:

```python
for piece in game.board.pieces:
	piece.player #1 or 2
	piece.other_player #1 or 2
	piece.bobail #True or False
	piece.captured #True or False
	piece.position #1-25
	piece.get_possible_moves() #[[int, int], [int, int], ...]
```

# Testing

Run `python3 -m unittest discover` from the root.

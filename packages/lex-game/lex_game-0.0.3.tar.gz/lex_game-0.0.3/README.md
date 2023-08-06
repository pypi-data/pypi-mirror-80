# LEX --- Learning EX-a-pawn

A game written by Mattia Monga for a 'Coding for lawyers' course. Copyright
2020 - Free to distribute, use, and modify according to the terms of
[GPLv3](LICENSE).

The code is simplistic but this version uses an OOP style; see branch
[master](https://gitlab.com/mmonga/lex/-/tree/master) for an even simpler
approach. 


## Installation

```
pip install lex_game
```

`lex_game -h` gives help on command line arguments.


## Rules of the game

Pawns move and capture as in chess, but there are neither two-step moves nor en-passant captures.
Players win by reaching the last row or by blocking the opponent.
Moves are given by two letters: the starting column and the ending one.

## Machine learning

Automatic players can learn to play better by memorizing its experience in Excel
files (the format was chosen as an example of using Python with spreadsheets).

With the command:
```
lex_game -e2 exapawn-empty.xlsx exapawn-001.xlsx
```

player 2 plays with the experience found in `exapawn-empty.xlsx`, at the end of 
the match, all the learned experience is saved in `exapawn-001.xlsx`.

It is possibile to make two automatic player play one against the other, see
`learn1vs2.sh` for a match with several games. After a dozen of games, player2
becomes unbeatable. This is a typical trend for a match with 30 games.

| game | Player 1 | Player 2 |
|------|----------|----------|
|    1 |        1 |          |
|    2 |        2 |          |
|    3 |        3 |          |
|    4 |        3 |        1 |
|    5 |        3 |        2 |
|    6 |        3 |        3 |
|    7 |        3 |        4 |
|    8 |        3 |        5 |
|    9 |        4 |        5 |
|   10 |        4 |        6 |
|   11 |        5 |        6 |
|   12 |        5 |        7 |
|   13 |        6 |        7 |
|   14 |        6 |        8 |
|   15 |        6 |        9 |
|   16 |        6 |       10 |
|   17 |        6 |       11 |
|   18 |        6 |       12 |
|   19 |        6 |       13 |
|   20 |        6 |       14 |
|   21 |        6 |       15 |
|   22 |        6 |       16 |
|   23 |        6 |       17 |
|   24 |        7 |       17 |
|   25 |        7 |       18 |
|   26 |        7 |       19 |
|   27 |        7 |       20 |
|   28 |        7 |       21 |
|   29 |        7 |       22 |
|   30 |        7 |       23 |

The game can also be solved deterministically. See
[tree-solved](tree-solved.pdf) for a spoiler of the three pawns version. With
four or five paws for each player the game tree is much bigger, but nevertheless
it can be produced by the program in a few minutes.

### References

See: https://www.gwern.net/docs/rl/1991-gardner-ch8amatchboxgamelearningmachine.pdf

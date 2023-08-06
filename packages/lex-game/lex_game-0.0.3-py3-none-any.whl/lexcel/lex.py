"""LEX board operations."""

EMPTY = 0
CYAN = 1
VIOLET = 2

MARKS = (' ', '♙', '♟')

DIGITS = "0123456789ABCDEFGHIJKLMNOPQ"


def other(player):
    """Return opposite color. """
    if player == VIOLET:
        return CYAN
    if player == CYAN:
        return VIOLET
    return EMPTY

def pawns_to_code(pawns_dict):
    """Return an alphanumeric representation of a board for ease board matching.

    The code is a string of alphanumeric digits representing columns,
    therefore a flipped board has exactly the reverse code.

    """
    r = ''
    base = VIOLET+1
    assert len(DIGITS) == base**3, len(DIGITS) # pragma: no mutate
    for c in sorted(pawns_dict.keys()):
        n = 0
        for i, p in enumerate(pawns_dict[c]):
            n += p * base**i
        r += DIGITS[n]
    return r.upper()


class Board:
    """All the Boards in a program must have the same number of columns and rows.
    """

    COLS = []

    @classmethod
    def _init_board_params(cls, ncols, nrows=3):
        """Init globals used for Board instantiation."""
        col_names = ('V', 'W', 'X', 'Y', 'Z')
        cls.NROWS = nrows
        cls.COLS = tuple(col_names[-ncols:])
        cls.WELL_FORMED_MOVES = []
        for i in cls.COLS:
            for j in cls.COLS:
                if abs(ord(i) - ord(j)) <= 1:
                    cls.WELL_FORMED_MOVES.append(i+j)
        cls.WELL_FORMED_MOVES = tuple(cls.WELL_FORMED_MOVES)

    def _pawns_from_code(self, h):
        """Return a dict corresponding to code digits.
        """
        assert len(self.COLS) == len(h), "{} {}".format(self.COLS, h) # pragma: no mutate
        r = {}
        base = VIOLET + 1
        for i, c in enumerate(self.COLS):
            col = []
            n = int(h[i], base=base**3)
            for _ in range(self.NROWS):
                col.append(n % base)
                n = n // base
            r[c] = tuple(col)

        return r

    def __init__(self, code=None, ncols=3):
        if code is None:
            code = 'B'*ncols
        else:
            ncols = len(code)

        assert ncols == len(code), '{} {}'.format(ncols, code) # pragma: no mutate
        if Board.COLS == [] or len(Board.COLS) != len(code):
            Board._init_board_params(len(code))

        self.pawns = self._pawns_from_code(code)

    def __str__(self):
        """Return a string representation for the board.

        It uses Unicode code points for 'WHITE CHESS PAWN' and 'BLACK CHESS PAWN'.
        """

        def add_hline(line):
            line = line + ' '
            for _ in self.COLS:
                line = line + '+---'
            line = line + '+\n'
            return line


        s = '\n '
        for c in self.COLS:
            s = s + '  ' + c + ' '
        s = add_hline(s + ' \n')

        for r in range(self.NROWS):
            for c in self.COLS:
                s = s + ' | {}'.format(MARKS[self[c][r]])
            s = s + ' |\n'
            s = add_hline(s)
        s = s + 'Board code: {}\n'.format(self.get_code())
        return s

    def __eq__(self, other_object):
        if not isinstance(other_object, Board):
            return NotImplemented
        return hash(self) == hash(other_object)

    def __hash__(self):
        return int(pawns_to_code(self.pawns), len(DIGITS))

    def get_code(self):
        """Return the code which identifies this board."""
        x = hash(self)
        base = len(DIGITS)
        r = ''
        for _ in range(len(self.COLS)):
            r = DIGITS[x % base] + r
            x = x // base
        return r

    def __getitem__(self, col):
        return self.pawns[col]

    def __setitem__(self, col, value):
        raise TypeError("'Board' objects are immutable!")


    def flip(self):
        """Return a board with the columns flipped.
        """
        return Board(self.get_code()[::-1])

    def flip_move(self, move):
        """Return a flipped move, i.e. the move according to the board with flipped colums.
        """
        r = ''
        for c in move:
            for i, k in enumerate(self.COLS):
                if c == k:
                    r = r + self.COLS[-(i+1)]
        return r

    def exchange(self):
        """Return a board with players exchanged as if VIOLET played as CYAN and viceversa.
        """
        b = {}
        for c in self.COLS:
            b[c] = [EMPTY, EMPTY, EMPTY]
            for i, p in enumerate(self[c][::-1]):
                b[c][i] = other(p)
            b[c] = tuple(b[c])
        return Board(pawns_to_code(b))

    def can_move_fwd(self, player, column):
        """True if player can move forward in column.
        """
        if player == VIOLET:
            for row in range(self.NROWS-1):
                if self[column][row] == VIOLET and self[column][row+1] == EMPTY:
                    return True
            return False
        return self.exchange().can_move_fwd(VIOLET, column)

    def can_capture(self, player, column):
        """True if player can move diagonally from column and capture a pawn of the other color.
        """
        if player == VIOLET:
            if column == self.COLS[0]:
                for row in range(Board.NROWS-1):
                    if self[self.COLS[0]][row] == VIOLET and self[self.COLS[1]][row + 1] == CYAN:
                        return True
            elif column == self.COLS[-1]:
                return self.flip().can_capture(VIOLET, self.COLS[0])
            else:
                c = self.COLS.index(column)
                for row in range(self.NROWS-1):
                    if self[column][row] == VIOLET and CYAN in (self[self.COLS[c-1]][row + 1],
                                                                self[self.COLS[c+1]][row + 1]):
                        return True
            return False
        return self.exchange().can_capture(VIOLET, column)

    def is_winner(self, player):
        """True if player is winning. """
        if player == VIOLET:
            opponent_moves = 0
            for c in self.COLS:
                if self[c][-1] == VIOLET:
                    return True
                if self.can_move_fwd(CYAN, c) or self.can_capture(CYAN, c):
                    opponent_moves += 1
            return opponent_moves == 0
        return self.exchange().is_winner(VIOLET)

    class IllegalMoveError(Exception):
        """An illegal move was tried."""

    def move(self, player, start, end):
        """Return a board in which player has moved from columns start to column end.

        Raise an exception if the move is not legal.
        """
        assert start+end in self.WELL_FORMED_MOVES # pragma: no mutate

        b = {}
        for c in self.COLS:
            b[c] = self[c]

        if player == VIOLET:
            if start == end and not self.can_move_fwd(VIOLET, start):
                raise Board.IllegalMoveError(
                    "{} cannot move forward on column {}".format(VIOLET, start))
            if start == end:
                if not self.can_move_fwd(VIOLET, start):
                    raise Board.IllegalMoveError('Invalid forward move.')
                col = list(self[start])
                i = len(col) - 1 - col[::-1].index(VIOLET)
                col[i] = EMPTY
                col[i + 1] = VIOLET
                b[start] = tuple(col)
                return Board(pawns_to_code(b))

            if not self.can_capture(VIOLET, start):
                raise Board.IllegalMoveError('Invalid capture move.')

            def capture(bdict, from_row, to_row):
                if self[start][from_row] == VIOLET and self[end][to_row] == CYAN:
                    bdict[start] = list(self[start])
                    bdict[end] = list(self[end])
                    bdict[start][from_row] = EMPTY
                    bdict[end][to_row] = VIOLET
                    bdict[start] = tuple(bdict[start])
                    bdict[end] = tuple(bdict[end])
                    return Board(pawns_to_code(bdict))
                return None

            for row in range(self.NROWS-1):
                r = capture(b, row, row + 1)
                if r is not None:
                    return r

            raise Board.IllegalMoveError("No move is possible!")

        return self.exchange().move(VIOLET, start, end).exchange()

    def is_symmetrical(self):
        """True if board is symmetric."""
        return self == self.flip()


    def get_legal_moves(self, player):
        """Return a list of all legal moves for player in a given board position."""
        r = []
        for m in self.WELL_FORMED_MOVES:
            try:
                self.move(player, m[0], m[1])
                r.append(m)
            except Board.IllegalMoveError:
                pass
        return r

    def prune_sym_moves(self, moves):
        """Return a list of moves filtered for symmetrical ones."""
        if len(moves) <= 1:
            return moves
        if self.flip_move(moves[0]) in moves[1:]:
            return self.prune_sym_moves(moves[1:])
        return self.prune_sym_moves(moves[1:]) + [moves[0]]

    @classmethod
    def get_forest(cls, ncols):
        """Return a string with a LaTeX game tree and the set of unique boards.

        Boards are returned as a dictionary with the lists of turns in which each appears.
        """

        boards = {}

        def get_tree(board, player, turn, a_move, indent):
            code = board.get_code()
            if board.is_winner(other(player)):
                s = "{}[{},winner{},move={{{}}}{{{}}}]".format(indent, code,
                                                               other(player),
                                                               other(player), a_move.lower())
                return s, other(player)
            moves = board.get_legal_moves(player)
            if board.is_symmetrical():
                moves = board.prune_sym_moves(moves)
            if code in boards:
                for m in moves:
                    boards[code][1].add(m)
            elif code[::-1] in boards:
                for m in moves:
                    boards[code[::-1]][1].add(board.flip_move(m))
            else:
                boards[code] = (turn, set(moves))
            s = "{}[{},winner@".format(indent, code)
            if a_move is not None:
                s = s + ",move={{{}}}{{{}}},winner@".format(other(player), a_move.lower())
            s = s + "\n"
            winners = []
            for m in moves:
                b = board.move(player, m[0], m[1])
                t, w = get_tree(b, other(player), turn+1, m, indent + " ")
                s = s + t + "\n"
                winners.append(w)
            if len(set(winners)) == 1:
                winner = winners[0]
            else:
                winner = player
            s = s.replace('@', str(winner))
            return s + indent + "]", winner

        f = """
%% Game tree for LEX --- Learning EX-a-pawn
%% Uncomment the lines which begin with % for a standalone LaTeX document
%\\documentclass[tikz]{standalone}
%\\usepackage{forest}
%\\begin{document}

\\forestset{
  default preamble={
    for tree={font=\\tiny}
  }
}
\\begin{forest}
  winner1/.style={draw,fill=cyan,inner sep=1pt,outer sep=0},
  winner2/.style={draw,fill=violet!60,inner sep=1pt,outer sep=0},
  move/.style n args=2{%
    if={#1<2}%
    {edge label/.expanded={%
      node [midway,fill=white,text=cyan,font=\\unexpanded{\\tiny}] {$#2$}%
    }}{edge label/.expanded={%
      node [midway,fill=white,text=violet!60,font=\\unexpanded{\\tiny}] {$#2$}%
    }},
  }
"""
        t, _ = get_tree(Board(ncols=ncols), CYAN, 1, None, " ")
        f = f + t
        f = f + "\n\\end{forest}"
        f = f + "\n%\\end{document}"

        for h in boards:
            b = Board(h)
            if b.is_symmetrical():
                moves = b.prune_sym_moves(list(boards[h][1]))
                boards[h] = (boards[h][0], set(moves))

        return f, boards

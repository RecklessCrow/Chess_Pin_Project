import itertools
import random
from time import time

import chess

PIECE_MAP = {
    'knight': chess.KNIGHT,
    'bishop': chess.BISHOP,
    'rook': chess.ROOK,
    'king': chess.KING,
    'queen': chess.QUEEN,
    'pawn': chess.PAWN
}

SQUARES = []
BLACK_SQUARES = []

# Generate lists of SQUARES and BLACK_SQUARES
odd_row = True
for letter in 'ABCDEFGH':

    for number in range(1, 9):
        SQUARES.append(eval(f'chess.{letter}{number}'))

    r = range(1, 9, 2) if odd_row else range(2, 9, 2)

    for number in r:
        BLACK_SQUARES.append(eval(f'chess.{letter}{number}'))

    odd_row = not odd_row

SQUARES.sort()
BLACK_SQUARES.sort()


def find_solution(board, black_square, black_piece, white_piece):
    """
    Find the minimum number of white pieces required to pin the black piece
    :param board:
    :param black_square:
    :param black_piece:
    :param white_piece:
    :return:
    """

    def black_is_pinned(white_positions):
        """
        Check if black piece is pinned given a list of white positions
        :param white_positions:
        :return:
        """
        # skip case where we try to place a white piece on top of the black piece
        if black_square in white_positions:
            return False

        board.clear()
        board.turn = chess.BLACK

        # add pieces to board
        board.set_piece_at(black_square, black_piece)
        for pos in white_positions:
            board.set_piece_at(pos, white_piece)

        # if black has no legal moves, then it's pinned
        if not board.legal_moves:
            return True

        for move in board.legal_moves:
            # make black move
            board.push(move)

            # if blacks ending position is not covered in whites possible move set, return false
            if str(move)[2:] not in {str(move)[2:] for move in board.legal_moves}:
                return False

            # undo move
            board.pop()

        return True

    # Iterate over all possible combinations of white positions starting with 1 piece, then 2, so forth and so on
    # An issue with this is that it takes a while if the required number of pieces is greater than 5
    # possible search space is 2 ^ 64 so it would take years to exhaust
    for i in range(len(SQUARES)):
        for white_positions in itertools.combinations(SQUARES, i):
            if black_is_pinned(white_positions):
                return white_positions

    return []


def print_board(black, white):
    """
    Print out the solution to pin the black piece
    :param black:
    :param white:
    :return:
    """

    # make board
    board = chess.Board()
    board.clear()

    # make black piece
    piece_type = PIECE_MAP[black]
    piece_color = chess.BLACK
    black_piece = chess.Piece(color=piece_color, piece_type=piece_type)

    # make white piece
    piece_type = PIECE_MAP[white]
    piece_color = chess.WHITE
    white_piece = chess.Piece(color=piece_color, piece_type=piece_type)

    # select random black square
    rand_black_square = random.choice(BLACK_SQUARES)

    # find and time the solution
    start = time()
    solution = find_solution(board, rand_black_square, black_piece, white_piece)
    end = time()

    # place pieces on board
    board.clear()
    board.set_piece_at(rand_black_square, black_piece)

    # print out the solution
    if solution:
        for square in solution:
            board.set_piece_at(square, white_piece)

        print()
        print(board, '\n')
        print(f'Minimum number of white {white}s required: {len(solution)}')
        print(f'Took {end - start:.2f} seconds.')

    # Realistically impossible to get here
    else:
        print(board, '\n')
        print('No solution found.')


if __name__ == '__main__':
    print_board('knight', 'knight')

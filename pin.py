import itertools
import os
import random
from time import time

import chess
import chess.svg

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


def find_solution(black_square, black_piece, white_piece):
    """
    Find the minimum number of white pieces required to pin the black piece
    :param carry:
    :param black_square:
    :param black_piece:
    :param white_piece:
    :return:
    """

    board = chess.Board()
    board.clear()

    def black_is_pinned(white_positions):
        """
        Check if black piece is pinned given a list of white positions
        :param white_positions:
        :return:
        """
        # skip case where we try to place a white piece on top of the black piece
        if black_square in white_positions:
            return False

        board = chess.Board()
        board.clear()
        board.turn = chess.BLACK

        # add pieces to board
        board.set_piece_at(black_square, black_piece)
        black_moves = list(board.legal_moves)

        for pos in white_positions:
            board.set_piece_at(pos, white_piece)

        # if black has no legal moves, then it's pinned
        if not board.legal_moves:
            return True

        for move in black_moves:
            # make black move
            board.push(move)

            # if blacks ending position is not covered in whites possible move set, return false
            if str(move)[2:] not in {str(move)[2:] for move in board.legal_moves}:
                return False

            # undo move
            board.pop()

        return True

    # get only squares where the pieces are going to intersect with the resulting black move
    board.clear()

    board.turn = chess.BLACK
    board.set_piece_at(black_square, black_piece)
    black_moves = [eval(f'chess.{str(move)[2:].upper()}') for move in board.legal_moves if len(str(move)) <= 4]

    # Take into account the case where the black piece is a pawn and is one square away from being able to promote
    if black_piece.piece_type == chess.PAWN and chess.A2 <= black_square <= chess.H2:
        for letter in 'ABCDEFGH':
            if black_square == eval(f'chess.{letter}2'):
                black_moves = [eval(f'chess.{letter}1')]
                break

    board.clear()
    board.turn = chess.WHITE
    possible_white_squares = set(black_moves)

    for square in SQUARES:
        if square == black_square:
            continue

        board.set_piece_at(square, white_piece)

        for move in board.legal_moves:
            if len(str(move)) > 4:
                continue

            move = eval(f'chess.{str(move)[2:].upper()}')

            if move in black_moves:
                possible_white_squares.add(square)
                break

        board.clear()

    if not black_moves:
        return []

    # Iterate over all possible combinations of white positions starting with 1 piece, then 2, so forth and so on
    # An issue with this is that it takes a while if the required number of pieces is greater than 5
    # Largest possible search space is 2 ^ 64 so it would take ages to exhaust
    for i in range(1, len(possible_white_squares) + 1):

        for white_positions in itertools.combinations(possible_white_squares, i):
            if black_is_pinned(white_positions):
                return white_positions

    board.clear()
    board.set_piece_at(black_square, black_piece)
    raise Exception(f"No solution possible for this board.\n{board}")


def print_board(black, white):
    """
    Print out the solution to pin the black piece
    :param black:
    :param white:
    :return:
    """

    # make black piece
    black_piece = chess.Piece(color=chess.BLACK, piece_type=PIECE_MAP[black])
    # make white piece
    white_piece = chess.Piece(color=chess.WHITE, piece_type=PIECE_MAP[white])

    # select random black square
    rand_black_square = random.choice(BLACK_SQUARES)

    # find and time the solution
    start = time()
    solution = find_solution(rand_black_square, black_piece, white_piece)
    end = time()

    # place pieces on board
    board = chess.Board()
    board.clear()
    board.set_piece_at(rand_black_square, black_piece)

    # print out the solution
    for square in solution:
        board.set_piece_at(square, white_piece)

    run_time = end - start
    if run_time < 60:
        run_time = f'{end - start:.2f} seconds'
    elif run_time < 60 * 60:
        m = int(run_time // 60)
        run_time = f'{m} {"minutes" if m > 1 else "minute"} and {run_time % 60:.2f} seconds'
    else:
        run_time = f'lmao'

    print()
    print(board, '\n')
    print(f'Minimum number of white {white}s required: {len(solution)}')
    print(f'Took {run_time} to solve.\n')

    # Draw the board
    img_path = os.path.join('images', 'chess_board.svg')
    with open(img_path, 'w+') as f:
        f.write(chess.svg.board(board))


if __name__ == '__main__':
    # print_board('knight', 'knight')
    # print_board('king', 'king')
    # print_board('rook', 'rook')
    # print_board('bishop', 'bishop')
    # print_board('queen', 'queen')
    pass

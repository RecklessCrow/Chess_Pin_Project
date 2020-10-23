import itertools
from time import time
import chess
import random

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
    def black_is_pinned(white_positions):
        board.clear()

        # add pieces to board
        board.set_piece_at(black_square, black_piece)

        if black_square in white_positions:
            return False

        for pos in white_positions:
            board.set_piece_at(pos, white_piece)

        board.turn = chess.BLACK

        if not board.legal_moves:
            return True

        for move in board.legal_moves:
            # make black move
            # if move is not covered in whites possible moveset return false
            pos = str(move)[2:]
            board.push(move)

            if pos not in [str(move)[2:] for move in board.legal_moves]:
                return False

            board.pop()

        return True

    for i in range(len(SQUARES)):
        for white_positions in itertools.combinations(SQUARES, i):
            if black_is_pinned(white_positions):
                return white_positions

    return []


def calculate_pin(black, white):
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

    start = time()
    solution = find_solution(board, rand_black_square, black_piece, white_piece)
    end = time()

    board.clear()
    board.set_piece_at(rand_black_square, black_piece)
    for square in solution:
        board.set_piece_at(square, white_piece)

    print()
    print(board, '\n')
    print(f'Took {end - start:.2f} seconds.')


if __name__ == '__main__':
    calculate_pin('queen', 'knight')

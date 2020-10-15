import chess
import random

PIECE_MAP = {'knight': chess.KNIGHT,
             'bishop': chess.BISHOP,
             'rook': chess.ROOK,
             'king': chess.KING,
             'queen': chess.QUEEN,
             'pawn': chess.PAWN
             }

BLACK_SQUARES = []

odd_row = True
for letter in 'ABCDEFGH':
    if odd_row:
        for number in range(1, 9, 2):
            BLACK_SQUARES.append(eval(f'chess.{letter}{number}'))
    else:
        for number in range(2, 9, 2):
            BLACK_SQUARES.append(eval(f'chess.{letter}{number}'))

    odd_row = not odd_row

BLACK_SQUARES.sort()


def calculate_pin(black, white):
    board = chess.Board()
    board.clear()
    board.turn = chess.BLACK

    piece_type = PIECE_MAP[black]
    piece_color = chess.BLACK
    black_piece = chess.Piece(color=piece_color, piece_type=piece_type)

    piece_type = PIECE_MAP[white]
    piece_color = chess.WHITE
    white_piece = chess.Piece(color=piece_color, piece_type=piece_type)

    rand_black_square = random.choice(BLACK_SQUARES)

    board.set_piece_at(rand_black_square, black_piece)

    moves = [move for move in board.generate_legal_moves()]

    # do BFS with goal of no legal moves and least number of white pieces

    print(board)


if __name__ == '__main__':
    calculate_pin('pawn', 'pawn')

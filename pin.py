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


class Graph:
    def __init__(self, num_nodes):
        self.nodes = {i + 1: [] for i in range(num_nodes)}

    def __str__(self):
        return str(self.nodes)

    def neighbors(self, node):
        return self.nodes[node]

    def add_edge(self, start, end, cost):
        self.nodes[end].append((start, cost))


def bfs(graph, start, goal):
    # keep track of unvisited nodes, the path taken, and the cost of the path
    open_list = deque()
    closed_list = {}
    visited = [goal]
    open_list.append((goal, 0, visited))
    path = []
    path_cost = float('-inf')

    while open_list:
        current_node, current_cost, current_visited = open_list.pop()

        for next_node, cost in graph.neighbors(current_node):

            new_cost = cost ** current_cost if current_cost != 0 else cost

            if next_node not in closed_list or new_cost > closed_list[next_node]:
                closed_list[next_node] = new_cost
                open_list.append((next_node, new_cost, current_visited + [next_node]))

            if next_node == start:
                # todo: check for lexicographical order if costs are equal
                if new_cost > path_cost:
                    path = current_visited + [next_node]
                    path_cost = new_cost

    path.reverse()

    return path, path_cost


def calculate_pin(black, white):
    # make board
    board = chess.Board()
    board.clear()
    board.turn = chess.BLACK

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

    board.set_piece_at(rand_black_square, black_piece)
    move_set = {str(move)[2:] for move in board.legal_moves}
    board.turn = chess.WHITE

    board.set_piece_at(rand_black_square + 1, white_piece)
    piece_move_set = {str(move)[2:] for move in board.legal_moves}

    # if one move of a white piece intersects with a legal move, save white piece keep searching
    # go through all squares of board, try adding a white piece?

    # do BFS with goal of no legal moves and least number of white pieces

    print(board)


if __name__ == '__main__':
    calculate_pin('knight', 'queen')

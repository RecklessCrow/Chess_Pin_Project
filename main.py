from termcolor import colored

import pin

PIECES = ['pawn', 'rook', 'knight', 'bishop', 'king', 'queen']
SELECTIONS = {1: 'Start a new game',
              2: 'Redo last game',
              3: 'Exit'}

INVALID_PIECE = ' is an invalid piece type.\n'

last_black = None
last_white = None


def start_new_pin_calc(redo=False):
    """
    Interact with user to generate a new game
    :return:
    """
    global last_black, last_white

    if not redo:
        black_type = input("Enter the black piece type: ")
        black_type = black_type.lower()

        while black_type not in PIECES:
            print(colored(black_type + INVALID_PIECE, 'red'))
            black_type = input("Enter the black piece type: ")

        white_type = input("Enter the white piece type: ")
        white_type = white_type.lower()

        while white_type not in PIECES:
            print(colored(white_type + INVALID_PIECE, 'red'))
            white_type = input("Enter the white piece type: ")

        last_black = black_type
        last_white = white_type

    else:
        black_type = last_black
        white_type = last_white

    pin.print_board(black_type, white_type)


def main():
    """
    Main function
    :return:
    """

    while True:
        print('Selections:')

        for i, selection in SELECTIONS.items():
            print(f'\t{i}) {selection}')

        selection = input("Enter your selection: ")

        invalid_selection = f"{selection} is an invalid selection. Please try again with a valid numerical selection.\n"

        try:
            selection = int(selection)
        except ValueError:
            print(colored(invalid_selection, 'red'))
            continue

        if selection not in SELECTIONS:
            print(colored(invalid_selection, 'red'))
            continue

        if SELECTIONS[selection] == 'Start a new game':
            start_new_pin_calc()

        elif SELECTIONS[selection] == 'Redo last game':
            if last_black is None:
                print(colored('No games have been played yet. Please play a game to use this option.\n', 'red'))
                continue

            start_new_pin_calc(redo=True)

        elif SELECTIONS[selection] == 'Exit':
            return


if __name__ == '__main__':
    main()

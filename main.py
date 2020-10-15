import pin
from termcolor import colored

PIECES = ['pawn', 'rook', 'knight', 'bishop', 'king', 'queen']
SELECTIONS = {1: 'Start a new game',
              2: 'Exit'}

INVALID_PIECE = ' is an invalid piece type.\n'


def main():
    while True:
        selection = input(f"Selections:\n"
                          f"\t1) {SELECTIONS[1]}\n"
                          f"\t2) {SELECTIONS[2]}\n\n"
                          f"Enter your selection: ")

        invalid_selection = f"{selection} is an invalid selection. Please try again.\n"

        try:
            selection = int(selection)
        except ValueError:
            print(colored(invalid_selection, 'red'))
            continue

        if selection not in SELECTIONS:
            print(colored(invalid_selection, 'red'))
            continue

        if SELECTIONS[selection] == 'Exit':
            return

        black_type = input("Enter the black piece type: ")
        black_type = black_type.lower()

        while black_type not in PIECES:
            print(colored(black_type + INVALID_PIECE, 'red'))
            black_type = input("Enter the black piece type: ")

        white_type = input("Enter the white piece type: ")
        white_type = white_type.lower()

        while white_type not in PIECES:
            print(colored(white_type + INVALID_PIECE, 'red'))
            white_type = input("Enter the black piece type: ")

        pin.calculate_pin(black_type, white_type)


if __name__ == '__main__':
    main()

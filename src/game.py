from src.board import Board
from src.player import Player, AIPlayer
from src.utils import clear_screen


class Game:
    def __init__(self):
        self.board = Board()

        print("1 - Player vs Player")
        print("2 - Player vs Computer")

        choice = input("Choose mode: ").strip()

        if choice == "1":
            name1 = input("Enter name for Player 1: ")
            name2 = input("Enter name for Player 2: ")

            self.player1 = Player(name1, "X")
            self.player2 = Player(name2, "O")

        elif choice == "2":
            name = input("Enter your name: ")

            print("Choose difficulty:")
            print("1 - Easy")
            print("2 - Medium")
            print("3 - Hard")

            diff_choice = input("Select: ")

            if diff_choice == "1":
                difficulty = "easy"
            elif diff_choice == "2":
                difficulty = "medium"
            else:
                difficulty = "hard"

            self.player1 = Player(name, "X")
            self.player2 = AIPlayer("Computer", "O", difficulty)

        else:
            print("Invalid choice, defaulting to Player vs Player")
            self.player1 = Player("Player 1", "X")
            self.player2 = Player("Player 2", "O")

        self.current_player = self.player1

    def switch_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def check_winner(self):
        b = self.board.grid

        winning_combinations = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]
        ]

        for combo in winning_combinations:
            if b[combo[0]] == b[combo[1]] == b[combo[2]] != " ":
                return True

        return False

    def play(self):
        clear_screen()
        print("=== TIC-TAC-TOE ===")
        self.board.display_positions()

        input("Press Enter to start...")

        while True:
            clear_screen()
            self.board.display()

            position = self.current_player.get_move(self.board)

            if not self.board.make_move(position, self.current_player.symbol):
                print("Position already taken. Try again.")
                input("Press Enter to continue...")
                continue

            if self.check_winner():
                clear_screen()
                self.board.display()
                print(f"{self.current_player.name} wins!")
                break

            if self.board.is_full():
                clear_screen()
                self.board.display()
                print("It's a draw!")
                break

            self.switch_player()

        print("Game over.")
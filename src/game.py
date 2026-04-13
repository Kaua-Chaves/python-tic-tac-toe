from src.board import Board
from src.player import Player
from src.utils import clear_screen

class Game:
    def __init__(self):
        self.board = Board()
        name_x = input("Enter name for Player X: ")
        name_o = input("Enter name for Player O: ")
        self.player_x = Player(name_x, "X")
        self.player_o = Player(name_o, "O")
        self.current_player = self.player_x

    def switch_player(self):
        if self.current_player == self.player_x:
            self.current_player = self.player_o
        else:
            self.current_player = self.player_x

    def check_winner(self):
        b = self.board.board

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
        print("Welcome to Tic-Tac-Toe!")
        self.board.display_positions()

        while True:
            self.board.display()

            position = self.current_player.get_move()

            if not self.board.make_move(position, self.current_player.symbol):
                print("Position already taken. Try again.")
                continue

            if self.check_winner():
                self.board.display()
                print(f"{self.current_player.name} wins!")
                break

            if self.board.is_full():
                self.board.display()
                print("It's a draw!")
                break

            self.switch_player()
            
            clear_screen()
            

        print("Game over.")
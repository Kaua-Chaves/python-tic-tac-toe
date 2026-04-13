import random


class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def get_move(self, board):
        while True:
            try:
                position = int(input(f"{self.name} ({self.symbol}), choose position (0-8): "))

                if 0 <= position <= 8:
                    return position
                else:
                    print("Invalid position. Try again.")

            except ValueError:
                print("Please enter a number.")


class AIPlayer(Player):
    def get_move(self, board):
        print(f"{self.name} is thinking... 🤖")

        available_moves = [i for i, spot in enumerate(board.grid) if spot == " "]
        return random.choice(available_moves)
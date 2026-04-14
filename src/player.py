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
    def __init__(self, name, symbol, difficulty="easy"):
        super().__init__(name, symbol)
        self.difficulty = difficulty

    def get_move(self, board):
        print(f"{self.name} ({self.difficulty}) is thinking... 🤖")

        if self.difficulty == "easy":
            return self.random_move(board)

        elif self.difficulty == "medium":
            if random.random() < 0.5:
                return self.random_move(board)
            else:
                return self.smart_move(board)

        elif self.difficulty == "hard":
            return self.smart_move(board)

    # 👇 EASY
    def random_move(self, board):
        available = [i for i, v in enumerate(board.grid) if v == " "]
        return random.choice(available)

    # 👇 MÉDIO/DIFÍCIL
    def smart_move(self, board):
        # tentar ganhar
        for i in range(9):
            if board.grid[i] == " ":
                board.grid[i] = self.symbol
                if self.check_win(board):
                    board.grid[i] = " "
                    return i
                board.grid[i] = " "

        # bloquear jogador
        opponent = "X" if self.symbol == "O" else "O"
        for i in range(9):
            if board.grid[i] == " ":
                board.grid[i] = opponent
                if self.check_win(board):
                    board.grid[i] = " "
                    return i
                board.grid[i] = " "

        return self.random_move(board)

    def check_win(self, board):
        b = board.grid

        combos = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]

        for c in combos:
            if b[c[0]] == b[c[1]] == b[c[2]] != " ":
                return True
        return False
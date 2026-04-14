import random


class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def get_move(self, board):
        # não usado na GUI (apenas estrutura)
        pass


class AIPlayer(Player):
    def __init__(self, name, symbol, difficulty="easy"):
        super().__init__(name, symbol)
        self.difficulty = difficulty

    def get_move(self, board):
        if self.difficulty == "easy":
            return self.random_move(board)

        if self.difficulty == "medium":
            return self.random_move(board) if random.random() < 0.5 else self.smart_move(board)

        return self.smart_move(board)

    def random_move(self, board):
        available = [i for i, v in enumerate(board.grid) if v == " "]
        return random.choice(available)

    def smart_move(self, board):
        # tenta ganhar
        for i in range(9):
            if board.grid[i] == " ":
                board.grid[i] = self.symbol
                if self.check_win(board):
                    board.grid[i] = " "
                    return i
                board.grid[i] = " "

        # bloqueia inimigo
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
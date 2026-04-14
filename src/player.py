import random


class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol


class AIPlayer(Player):
    def __init__(self, name, symbol):
        super().__init__(name, symbol)

    def get_move(self, board, level=1):
        if level == 99:
            return self.minimax_move(board)

        if level == 1:
            return self.random_move(board)

        if level == 2:
            return self.random_move(board) if random.random() < 0.6 else self.smart_move(board)

        return self.smart_move(board)

    def random_move(self, board):
        available = [i for i, v in enumerate(board.grid) if v == " "]
        return random.choice(available)

    def smart_move(self, board):
        for i in range(9):
            if board.grid[i] == " ":
                board.grid[i] = self.symbol
                if self.check_win(board, self.symbol):
                    board.grid[i] = " "
                    return i
                board.grid[i] = " "

        opponent = "X" if self.symbol == "O" else "O"

        for i in range(9):
            if board.grid[i] == " ":
                board.grid[i] = opponent
                if self.check_win(board, opponent):
                    board.grid[i] = " "
                    return i
                board.grid[i] = " "

        return self.random_move(board)

    # 🧠 MINIMAX (DESAFIO)
    def minimax_move(self, board):
        best_score = -999
        best_move = None

        for i in range(9):
            if board.grid[i] == " ":
                board.grid[i] = self.symbol
                score = self.minimax(board, False)
                board.grid[i] = " "

                if score > best_score:
                    best_score = score
                    best_move = i

        return best_move

    def minimax(self, board, is_maximizing):
        if self.check_win(board, self.symbol):
            return 1

        opponent = "X" if self.symbol == "O" else "O"

        if self.check_win(board, opponent):
            return -1

        if " " not in board.grid:
            return 0

        if is_maximizing:
            best = -999
            for i in range(9):
                if board.grid[i] == " ":
                    board.grid[i] = self.symbol
                    score = self.minimax(board, False)
                    board.grid[i] = " "
                    best = max(best, score)
            return best
        else:
            best = 999
            for i in range(9):
                if board.grid[i] == " ":
                    board.grid[i] = opponent
                    score = self.minimax(board, True)
                    board.grid[i] = " "
                    best = min(best, score)
            return best

    def check_win(self, board, symbol):
        b = board.grid

        combos = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]

        for c in combos:
            if b[c[0]] == b[c[1]] == b[c[2]] == symbol:
                return True

        return False
from src.board import Board
from src.player import Player, AIPlayer


class Game:
    def __init__(self, mode, difficulty=1, name1="Player 1", name2="AI"):
        self.mode = mode
        self.difficulty = difficulty

        self.board = Board()

        self.player1 = Player(name1, "X")

        if mode == "pvp":
            self.player2 = Player(name2, "O")
        else:
            self.player2 = AIPlayer("AI", "O")

        self.current_player = self.player1

        self.winner = None
        self.finished = False
        self.win_combo = None

    def play_move(self, position):
        if self.finished:
            return False

        if not self.board.make_move(position, self.current_player.symbol):
            return False

        if self.check_winner():
            self.winner = self.current_player
            self.finished = True
            return True

        if self.board.is_full():
            self.finished = True
            return True

        self.switch_player()
        return True

    def switch_player(self):
        self.current_player = (
            self.player2 if self.current_player == self.player1 else self.player1
        )

    def check_winner(self):
        b = self.board.grid

        combos = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]

        for c in combos:
            if b[c[0]] == b[c[1]] == b[c[2]] != " ":
                self.win_combo = c
                return True

        self.win_combo = None
        return False
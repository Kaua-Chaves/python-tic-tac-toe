class Board:
    def __init__(self):
        self.grid = [" " for _ in range(9)]

    def make_move(self, position, player):
        if self.grid[position] == " ":
            self.grid[position] = player
            return True
        return False

    def is_full(self):
        return " " not in self.grid
    
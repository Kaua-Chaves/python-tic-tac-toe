class Board:
    def __init__(self):
        self.grid = [" " for _ in range(9)]

    def display(self):
        print()
        for i in range(9):
            value = self.grid[i] if self.grid[i] != " " else str(i)
            print(f" {value} ", end="")

            if i % 3 != 2:
                print("|", end="")
            else:
                print()
                if i != 8:
                    print("---+---+---")
        print()

    def display_positions(self):
        print()
        print(" 0 | 1 | 2 ")
        print("---+---+---")
        print(" 3 | 4 | 5 ")
        print("---+---+---")
        print(" 6 | 7 | 8 ")
        print()

    def make_move(self, position, player):
        if self.grid[position] == " ":
            self.grid[position] = player
            return True
        return False

    def is_full(self):
        return " " not in self.grid
    
    
import tkinter as tk
from tkinter import messagebox
from src.board import Board


class TicTacToeGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe")

        self.window.geometry("420x500")
        self.window.configure(bg="#1e1e1e")
        self.window.resizable(False, False)
        self.window.eval('tk::PlaceWindow . center')

        self.board = Board()
        self.current_player = "X"
        self.game_over = False

        self.buttons = []

        self.title = tk.Label(
            self.window,
            text="Tic-Tac-Toe",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#1e1e1e"
        )
        self.title.pack(pady=10)

        self.frame = tk.Frame(self.window, bg="#1e1e1e")
        self.frame.pack()

        self.create_grid()

        self.window.mainloop()

    def create_grid(self):
        for i in range(9):
            button = tk.Button(
                self.frame,
                text="",
                font=("Arial", 28, "bold"),
                width=4,
                height=2,
                bg="#2b2b2b",
                fg="white",
                activebackground="#3a3a3a",
                relief="flat",
                command=lambda i=i: self.make_move(i)
            )

            button.grid(row=i // 3, column=i % 3, padx=5, pady=5)

            button.bind("<Enter>", lambda e, b=button: b.config(bg="#3a3a3a"))
            button.bind("<Leave>", lambda e, b=button: b.config(bg="#2b2b2b"))

            self.buttons.append(button)

    def make_move(self, position):
        if self.game_over:
            return

        if self.board.grid[position] != " ":
            return

        self.board.grid[position] = self.current_player
        self.buttons[position]["text"] = self.current_player

        self.buttons[position]["fg"] = "#ff4d4d" if self.current_player == "X" else "#4da6ff"

        if self.check_winner():
            self.show_game_over(self.current_player)
            return

        if self.board.is_full():
            self.show_game_over("draw")
            return

        self.switch_player()

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        b = self.board.grid

        combos = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]
        ]

        for c in combos:
            if b[c[0]] == b[c[1]] == b[c[2]] != " ":
                return True
        return False

    # ⭐ MELHORIA PRINCIPAL
    def show_game_over(self, result):
        self.game_over = True

        if result == "draw":
            title = "🤝 Empate!"
            msg = "Deu velha!\n\nQuer jogar novamente?"
        else:
            title = "🏆 Vitória!"
            msg = f"🎉 Jogador {result} venceu!\n\nParabéns!"

        messagebox.showinfo(title, msg)
        self.reset_game()

    def reset_game(self):
        self.board = Board()
        self.current_player = "X"
        self.game_over = False

        for button in self.buttons:
            button.config(text="", fg="white")
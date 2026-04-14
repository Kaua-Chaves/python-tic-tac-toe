import tkinter as tk
from tkinter import messagebox
from src.game import Game


class TicTacToeGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe")

        self.window.geometry("450x600")
        self.window.configure(bg="#121212")
        self.window.resizable(False, False)
        self.window.eval('tk::PlaceWindow . center')

        self.game = None
        self.buttons = []

        self.show_menu()
        self.window.mainloop()

    # ---------------- MENU MODERNO ----------------
    def show_menu(self):
        self.clear()

        self.menu = tk.Frame(self.window, bg="#121212")
        self.menu.pack(expand=True)

        title = tk.Label(
            self.menu,
            text="TIC TAC TOE",
            font=("Helvetica", 28, "bold"),
            fg="#00ffd5",
            bg="#121212"
        )
        title.pack(pady=30)

        subtitle = tk.Label(
            self.menu,
            text="Choose your mode",
            font=("Helvetica", 12),
            fg="#aaaaaa",
            bg="#121212"
        )
        subtitle.pack(pady=5)

        self.mode = tk.StringVar(value="pvp")

        self.create_radio("PvP", "pvp")
        self.create_radio("PvC (AI)", "pvc")
        self.create_radio("🔥 Challenge (Impossible AI)", "challenge")

        start_btn = tk.Button(
            self.menu,
            text="START GAME",
            font=("Helvetica", 14, "bold"),
            bg="#00ffd5",
            fg="#000",
            activebackground="#00c2a8",
            padx=20,
            pady=8,
            bd=0,
            command=self.next
        )
        start_btn.pack(pady=25)

    def create_radio(self, text, value):
        tk.Radiobutton(
            self.menu,
            text=text,
            variable=self.mode,
            value=value,
            font=("Helvetica", 12),
            fg="white",
            bg="#121212",
            selectcolor="#1e1e1e",
            activebackground="#121212"
        ).pack(anchor="w", padx=60, pady=5)

    # ---------------- NEXT SCREEN ----------------
    def next(self):
        mode = self.mode.get()
        self.menu.destroy()

        self.config = tk.Frame(self.window, bg="#121212")
        self.config.pack(expand=True)

        tk.Label(
            self.config,
            text="Enter your name",
            fg="white",
            bg="#121212",
            font=("Helvetica", 14)
        ).pack(pady=10)

        self.p1 = tk.Entry(
            self.config,
            font=("Helvetica", 14),
            justify="center"
        )
        self.p1.pack(pady=10)

        tk.Button(
            self.config,
            text="START",
            font=("Helvetica", 12, "bold"),
            bg="#00ffd5",
            fg="black",
            bd=0,
            padx=15,
            pady=5,
            command=lambda: self.start(mode)
        ).pack(pady=20)

    # ---------------- START GAME ----------------
    def start(self, mode):
        name1 = self.p1.get() or "Player"

        self.config.destroy()

        self.game = Game(mode, "easy", name1, "AI")

        self.create_board()

    # ---------------- BOARD MODERNO ----------------
    def create_board(self):
        self.frame = tk.Frame(self.window, bg="#121212")
        self.frame.pack(expand=True)

        self.buttons = []

        self.status_label = tk.Label(
            self.window,
            text="Your turn",
            font=("Helvetica", 12),
            fg="#aaaaaa",
            bg="#121212"
        )
        self.status_label.pack(pady=10)

        for i in range(9):
            btn = tk.Button(
                self.frame,
                text="",
                font=("Helvetica", 26, "bold"),
                width=4,
                height=2,
                bg="#1f1f1f",
                fg="white",
                activebackground="#2a2a2a",
                relief="flat",
                bd=0,
                command=lambda i=i: self.move(i)
            )

            btn.grid(row=i // 3, column=i % 3, padx=6, pady=6)

            # 🎯 hover effect
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#2a2a2a"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#1f1f1f"))

            self.buttons.append(btn)

    # ---------------- MOVE ----------------
    def move(self, pos):
        if not self.game.play_move(pos):
            return

        self.animate_button(pos)
        self.update()

        if self.game.finished:
            self.end(self.game.winner.name if self.game.winner else "draw")
            return

        self.status_label.config(text="AI thinking...")
        self.window.after(200, self.ai)

    # ---------------- AI ----------------
    def ai(self):
        if self.game.current_player.name != "AI":
            return

        level = 99 if self.game.mode == "challenge" else 2

        pos = self.game.current_player.get_move(self.game.board, level)

        self.game.play_move(pos)

        self.animate_button(pos)
        self.update()

        self.status_label.config(text="Your turn")

        if self.game.finished:
            self.end(self.game.winner.name if self.game.winner else "draw")

    # ---------------- ANIMATION ----------------
    def animate_button(self, pos):
        btn = self.buttons[pos]
        btn.config(bg="#00ffd5", fg="black")
        self.window.after(150, lambda: btn.config(bg="#1f1f1f"))

    # ---------------- UPDATE ----------------
    def update(self):
        for i in range(9):
            self.buttons[i]["text"] = self.game.board.grid[i]

    # ---------------- END ----------------
    def end(self, result):

        if self.game.mode == "challenge":
            if result == "draw":
                msg = "🤝 Draw vs Impossible AI"
            elif result == "AI":
                msg = "🤖 AI defeated you!"
            else:
                msg = "🎉 You defeated Impossible AI!"

            messagebox.showinfo("Challenge Mode", msg)
            self.reset()
            return

        messagebox.showinfo("Game Over", f"{result} wins!")
        self.reset()

    # ---------------- RESET ----------------
    def reset(self):
        self.game = None
        self.buttons = []
        self.frame.destroy()
        self.status_label.destroy()
        self.show_menu()

    # ---------------- CLEAR ----------------
    def clear(self):
        for w in self.window.winfo_children():
            w.destroy()
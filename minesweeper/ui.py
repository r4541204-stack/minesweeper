"""Tkinter UI for Minesweeper."""

from __future__ import annotations

import tkinter as tk
# this is used for Pop-up Notification
from tkinter import messagebox

from .core import GameConfig, MinesweeperGame


# use a dictionary to save game difficulty level
DIFFICULTIES: dict[str, GameConfig] = {
    "Easy": GameConfig(9, 9, 10),
    "Medium": GameConfig(16, 16, 40),
    "Hard": GameConfig(16, 30, 99),
}

# use different colors to represent numbers
NUMBER_COLORS = {
    1: "#1d4ed8",
    2: "#15803d",
    3: "#b91c1c",
    4: "#1e3a8a",
    5: "#7c2d12",
    6: "#0f766e",
    7: "#111827",
    8: "#475569",
}


# this is for minesweeper GUI
class MinesweeperApp:
    """Graphical Minesweeper application."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root  # save passed in tk window
        self.root.title("Python Tkinter Minesweeper")  # set window title
        self.root.resizable(False, False)  # Resizing the window is prohibited.

        self.current_config = DIFFICULTIES["Easy"]  # set current level to easy
        self.game = MinesweeperGame(self.current_config)  # create game
        self.buttons: list[list[tk.Button]] = []  # 2d array, save all buttons on the board
        self.default_button_bg: str | None = None  # save background button color

        # these two used for binding text to a label
        self.status_var = tk.StringVar()
        self.mines_var = tk.StringVar()

        # build layout and start the game after configuration
        self._build_layout()  
        self.new_game(self.current_config)

    # build layout, build for __init__ to use it, not for user
    def _build_layout(self) -> None:
        # create a frame and set some padding
        container = tk.Frame(self.root, padx=10, pady=10)
        # used for show item on the frame, pack==show
        container.pack()

        # create top bar
        self.top_frame = tk.Frame(container)
        self.top_frame.pack(fill="x", pady=(0, 8))  # x means Horizontal Expansion

        # create level buttons
        for label, config in DIFFICULTIES.items():
            tk.Button(
                self.top_frame,
                text=label,
                width=8,
                command=lambda config=config: self.new_game(config),  # when user click this button, call self.new_game to start the game
            ).pack(side="left", padx=(0, 6))
        
        # create restart button
        tk.Button(
            self.top_frame,
            text="Restart",
            width=8,
            command=lambda: self.new_game(self.current_config),
        ).pack(side="left", padx=(0, 10))

        # create mines left tag, show remaining mines number
        tk.Label(
            self.top_frame,
            textvariable=self.mines_var,
            anchor="w",
            width=12,
        ).pack(side="left")

        # create status tag, show current game status
        tk.Label(
            self.top_frame,
            textvariable=self.status_var,
            anchor="w",
            width=24,
        ).pack(side="left")

        # after drawing, show board
        self.board_frame = tk.Frame(container, bd=2, relief=tk.GROOVE)
        self.board_frame.pack()

    # start a new game, with current config
    # 1. start new game 2. clear board 3. create new board button 4. refresh top bar labels
    def new_game(self, config: GameConfig) -> None:
        self.current_config = config
        self.game.new_game(config)
        self._clear_board()
        self._create_board()
        self._update_labels()

    # clear all buttons on the board, and set 2D array empty
    def _clear_board(self) -> None:
        for widget in self.board_frame.winfo_children():  # get all children widgets and destory them
            widget.destroy()
        self.buttons = []

    # create buttons on the board
    def _create_board(self) -> None:
        for row in range(self.game.rows):
            button_row: list[tk.Button] = []
            for col in range(self.game.cols):
                button = tk.Button(
                    self.board_frame,
                    width=2,
                    height=1,
                    text="", # show flag, mine, number in the future
                    font=("Segoe UI Emoji", 10, "bold"),
                    relief=tk.RAISED,  # style of the button, looks like Protruding
                    command=lambda row=row, col=col: self.handle_left_click(row, col),  # bind left click, also set current position
                )
                button.bind(
                    "<Button-3>",  # button 1 usually be left click, 3 be right click 
                    lambda _event, row=row, col=col: self.handle_right_click(row, col),  # bind right click 
                )
                button.grid(row=row, column=col, sticky="nsew")  # use grid to show button, because it's a board

                # also save default button background
                if self.default_button_bg is None:
                    self.default_button_bg = str(button.cget("bg"))
                button_row.append(button)
            self.buttons.append(button_row)

    # connect to core's left click, refresh cell status, update labels
    def handle_left_click(self, row: int, col: int) -> None:
        state = self.game.left_click(row, col)
        self._refresh_cells(state.changed)
        self._update_labels()

        # if win or lose, pop up message
        if state.game_over:
            self.status_var.set("Status: Lost")
            messagebox.showinfo("Game Over", "You clicked on a mine.")
        elif state.win:
            self.status_var.set("Status: Won")
            messagebox.showinfo("Congratulations", "You have cleared all safe cells.")

    # connect to core's right click, also refresh cell status, update labels
    def handle_right_click(self, row: int, col: int) -> str | None:
        state = self.game.right_click(row, col)
        self._refresh_cells(state.changed)
        self._update_labels()
        return "break" # Avoid triggering additional default behaviors.

    # refresh cells display
    def _refresh_cells(self, positions: set[tuple[int, int]]) -> None:
        for row, col in positions:
            self._refresh_cell(row, col)

    # refresh cell display
    def _refresh_cell(self, row: int, col: int) -> None:
        # get cell object from passed in position
        cell = self.game.get_cell(row, col)
        button = self.buttons[row][col] # get it's UI button

        # if cell is opened
        if cell.opened:
            # if cell is a mine, show it
            if cell.mine:
                button.config(
                    text="💣",
                    state=tk.DISABLED,
                    disabledforeground="#111827",
                    relief=tk.SUNKEN,
                    bg="#fecaca",
                )
                return
            # else, show number in the cell
            text = "" if cell.count == 0 else str(cell.count)
            button.config(
                text=text,
                state=tk.DISABLED,
                disabledforeground=NUMBER_COLORS.get(cell.count, "#111827"),
                relief=tk.SUNKEN,
                bg="#e5e7eb",
            )
            return

        # if the cell is flagged but not opened, show flag
        if cell.flagged:
            button.config(
                text="🚩",
                fg="#dc2626",
                state=tk.NORMAL,
                relief=tk.RAISED,
                bg=self.default_button_bg,
            )
        else:
            # if not flagged, show default way
            button.config(
                text="",
                fg="#111827",
                state=tk.NORMAL,
                relief=tk.RAISED,
                bg=self.default_button_bg,
            )
    # display status and remaining mines number at the top bar
    def _update_labels(self) -> None:
        if self.game.game_over:
            self.status_var.set("Status: Lost")
        elif self.game.win:
            self.status_var.set("Status: Won")
        elif self.game.first_click:
            self.status_var.set("Status: Waiting to Start")
        else:
            self.status_var.set("Status: In Progress")
        self.mines_var.set(f"Mines Left: {self.game.remaining_mines_estimate()}")

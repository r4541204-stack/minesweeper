"""Application entry point."""
# To make writing type hints more convenient and robust
from __future__ import annotations

# python gui package, it's used for create a window, button, tag, something like that
import tkinter as tk

from minesweeper.ui import MinesweeperApp

# -> None means that this function doesn't have a return value
def main() -> None:
    root = tk.Tk()    # create a tkinter windows object
    MinesweeperApp(root)   # create the whole minesweeper page
    root.mainloop()   # keep tkinter event in a loop, keep the windows running and waiting for user action


if __name__ == "__main__":
    main()
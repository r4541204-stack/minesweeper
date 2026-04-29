"""Minesweeper package."""
# Mark the `minesweeper` directory as a Python package, and define "what is exposed externally from this package."

from .core import Cell, GameConfig, GameState, MinesweeperGame

__all__ = ["Cell", "GameConfig", "GameState", "MinesweeperGame"]
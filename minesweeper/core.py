from __future__ import annotations

from collections import deque  # queue
from dataclasses import dataclass, field # store data
import random
from typing import Iterable  # used for type hints


@dataclass(frozen=True)
class GameConfig:
    rows: int
    cols: int
    mines: int

    def __post_init__(self) -> None:
        total_cells = self.rows * self.cols
        if self.rows <= 0 or self.cols <= 0:
            raise ValueError("rows and cols must be positive")
        if self.mines <= 0:
            raise ValueError("mines must be positive")
        if self.mines >= total_cells:
            raise ValueError("mines must be fewer than total cells")


@dataclass
class Cell:
    mine: bool = False
    opened: bool = False
    flagged: bool = False
    count: int = 0

@dataclass
class GameState:
    changed: set[tuple[int, int]] = field(default_factory=set)
    game_over: bool = False
    win: bool = False
    exploded: tuple[int, int] | None = None

class MinesweeperGame:
    def __init__(self, config: GameConfig, rng: random.Random | None = None) -> None:
        self.rng = rng or random.Random()
        self.new_game(config)

    def new_game(self, config: GameConfig) -> None:
        self.config = config
        self.rows = config.rows
        self.cols = config.cols
        self.mines = config.mines
        self.board = [
            [Cell() for _ in range(self.cols)]
            for _ in range(self.rows)
        ]
        self.first_click = True
        self.game_over = False
        self.win = False
        self.opened_count = 0

    def get_cell(self, row: int, col: int) -> Cell:
        self._validate_position(row, col)
        return self.board[row][col]

    def _validate_position(self, row: int, col: int) -> None:
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise IndexError("cell position out of bounds")

    def left_click(self, row: int, col: int) -> GameState:
        self._validate_position(row, col)
        state = GameState()

        if self.game_over or self.win:
            return state

        cell = self.board[row][col]
        if cell.opened or cell.flagged:
            return state

        if self.first_click:
            self.place_mines(row, col)
            self.calculate_counts()
            self.first_click = False

        if cell.mine:
            cell.opened = True
            state.changed.add((row, col))
            state.exploded = (row, col)
            self.game_over = True
            state.game_over = True
            state.changed.update(self.reveal_all_mines())
            return state

        state.changed.update(self.open_region(row, col))

        if self.check_win():
            self.win = True
            state.win = True
        return state

    def right_click(self, row: int, col: int) -> GameState:
        self._validate_position(row, col)
        state = GameState()

        if self.game_over or self.win:
            return state

        cell = self.board[row][col]
        if cell.opened:
            return state

        cell.flagged = not cell.flagged

        state.changed.add((row, col))
        return state

    def place_mines(self, first_row: int, first_col: int) -> None:
        positions = [
            (row, col)
            for row in range(self.rows)
            for col in range(self.cols)
            if(row, col) != (first_row, first_col)
        ]

        for row, col in self.rng.sample(positions, self.mines):
            self.board[row][col].mine = True

    def calculate_counts(self) -> None:
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.board[row][col]
                if cell.mine:
                    continue
                cell.count = sum(
                    1 for nr, nc in self.neighbors(row, col)
                    if self.board[nr][nc].mine
                )

    def open_region(self, start_row: int, start_col: int) -> set[tuple[int, int]]:
        changed: set[tuple[int, int]] = set()
        queue = deque([(start_row, start_col)])

        while queue:
            row, col = queue.popleft()
            cell = self.board[row][col]

            if cell.opened or cell.flagged:
                continue

            cell.opened = True
            changed.add((row, col))

            if not cell.mine:
                self.opened_count += 1

            if cell.count != 0:
                continue

            for nr, nc in self.neighbors(row, col):
                neighbor = self.board[nr][nc]
                if neighbor.opened or neighbor.flagged or neighbor.mine:
                    continue
                queue.append((nr, nc))

        return changed

    def neighbors(self, row: int, col: int) -> Iterable[tuple[int, int]]:
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr = row + dr
                nc = col + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    yield nr, nc

    def reveal_all_mines(self) -> set[tuple[int, int]]:
        changed: set[tuple[int, int]] = set()
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.board[row][col]
                if cell.mine and not cell.opened:
                    cell.opened = True
                    changed.add((row, col))

        return changed

    def check_win(self) -> bool:
        return self.opened_count == (self.rows * self.cols - self.mines)

    def remaining_mines_estimate(self) -> int:
        flagged = sum(
            1
            for row in self.board
            for cell in row
            if cell.flagged
        )
        return max(0, self.mines - flagged)
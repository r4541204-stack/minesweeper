# Minesweeper

A desktop Minesweeper game built with Python and `tkinter`.
The project separates the game rules from the GUI so the logic stays easy to test and the interface stays easy to maintain.

## Overview

This project includes:

- a `tkinter` graphical interface
- three preset difficulty levels
- safe first-click mine placement
- right-click flagging
- automatic blank-area expansion
- win/loss detection
- unit tests for the core game logic

## Gameplay

- Left click a cell to reveal it.
- Right click a cell to place or remove a flag.
- The first left click is always safe.
- If you reveal a mine, the game ends and all mines are shown.
- If you reveal every non-mine cell, you win.

## Difficulty Levels

| Difficulty | Board Size | Mines |
| --- | --- | --- |
| Easy | 9 x 9 | 10 |
| Medium | 16 x 16 | 40 |
| Hard | 16 x 30 | 99 |

## Interface

The top bar includes:

- difficulty buttons: `Easy`, `Medium`, `Hard`
- a `Restart` button
- a `Mines Left` counter based on the current flag count
- a status label such as `Waiting to Start`, `In Progress`, `Won`, or `Lost`

The board uses:

- colored numbers for revealed cells
- a flag icon for marked cells
- a mine icon for exploded and revealed mines

## Project Structure

```text
├── LICENSE
├── Project Design.md
├── README.md
├── main.py
└── minesweeper
   ├── __init__.py
   ├── core.py
   └── ui.py
 
```

## File Responsibilities

- `main.py`: application entry point that creates the `tkinter` window and starts the app
- `minesweeper/core.py`: pure game logic, including mine placement, cell opening, flagging, and win/loss checks
- `minesweeper/ui.py`: graphical interface and event handling
- `minesweeper/__init__.py`: package exports for the main game classes

## Requirements

- Python 3.10 or newer is recommended
- `tkinter` must be available in your Python installation

`tkinter` is included with most standard Python installations on Windows and macOS.
On some Linux systems, you may need to install it separately.

## How to Run

From the project root:

```bash
python main.py
```

If your system uses `python3` instead of `python`, run:

```bash
python3 main.py
```

## Run Tests

```bash
python -m unittest discover -s tests -v
```

Or, if needed:

```bash
python3 -m unittest discover -s tests -v
```
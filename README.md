````md
# 🎮 Connect 4 Console Game (Python AI)

A **console-based Connect 4 game** written in **Python**, featuring a **human player vs an AI opponent** powered by the **Minimax algorithm** with heuristic evaluation.

The game runs entirely in the terminal and demonstrates classic **game AI concepts** such as:
- Game state evaluation
- Minimax decision-making
- Depth-limited search
- Heuristic scoring

---

## 🧠 Features

- Standard **6×7 Connect 4 board**
- Human vs AI gameplay
- AI uses **Minimax algorithm** with configurable search depth
- Heuristic-based scoring system (offense + defense)
- Center-column prioritization (real Connect 4 strategy)
- Console-friendly board rendering
- Input validation & game-over detection

---

## 🛠️ Technologies Used

- **Python 3**
- Standard Library only:
  - `random`
  - `math`
  - `copy`

No external dependencies required.

---

## ⚙️ Game Configuration

You can easily tweak game behavior from the constants at the top of the file:

```python
ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER_PIECE = 'X'
AI_PIECE = 'O'
EMPTY = '-'

SEARCH_DEPTH = 4
````

* Increasing `SEARCH_DEPTH` makes the AI stronger (but slower)
* Board size and symbols are fully configurable

---

## 🤖 AI Logic Overview

### Minimax Algorithm

* The AI simulates future moves up to a fixed depth
* Assumes the human player always plays optimally
* Chooses the move that **maximizes its minimum guaranteed score**

### Heuristic Evaluation

The board is scored based on:

* Connecting 4 pieces (win)
* 3-in-a-row with open space
* 2-in-a-row setups
* Blocking opponent threats
* Center column control

---

## ▶️ How to Run

1. Make sure Python 3 is installed
2. Save the file as `connect4.py`
3. Run:

```bash
python connect4.py
```

---

## 🎯 How to Play

* You are **Player 1 (`X`)**
* The AI is **Player 2 (`O`)**
* On your turn, enter a column number:

```text
Player 1 Turn (Select Column 0-6):
```

* The board updates after every move
* First player to connect **4 pieces** wins

---

## 🖥️ Board Example

```
  0 1 2 3 4 5 6
----------------
| - - - - - - - |
| - - - - - - - |
| - - - - - - - |
| - - - O - - - |
| - - X X - - - |
| X O O X - - - |
----------------
```

---

## 📌 Project Purpose

This project is ideal for:

* Learning **game AI fundamentals**
* Understanding **Minimax & heuristics**
* Practicing **clean game logic design**
* Demonstrating algorithmic thinking in Python

---

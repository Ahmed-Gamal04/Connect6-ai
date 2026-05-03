# Connect 6 AI Game

An intelligent implementation of the **Connect 6 board game** using classic Artificial Intelligence search algorithms including **Minimax**, **Alpha-Beta Pruning**, and **Heuristic Evaluation**.

This project demonstrates how game-playing AI can make strategic decisions by analyzing future board states and selecting optimal moves.

---

## Project Overview

Connect 6 is a strategy board game where players compete to connect six consecutive pieces horizontally, vertically, or diagonally.

This project simulates the game with an AI opponent capable of making strong decisions using search algorithms commonly used in game theory and adversarial AI.

---

## AI Techniques Used

### Minimax Algorithm
Evaluates all possible future moves assuming both players play optimally.

### Alpha-Beta Pruning
Optimized version of Minimax that reduces unnecessary node evaluations, improving speed and efficiency.

### Heuristic Evaluation Function
Scores board positions when full search depth is not possible, allowing smarter decisions in complex states.

---

## Features

- Human vs AI gameplay
- Intelligent move selection
- GUI-based board interface
- Efficient search using Alpha-Beta pruning
- Custom heuristic evaluation
- Modular Python code structure

---

## Project Structure

```text
Connect6-AI/
│── alpha_beta.py      # Alpha-Beta pruning algorithm
│── minimax.py         # Minimax algorithm
│── heuristic.py       # Board evaluation function
│── board.py           # Board representation
│── game_logic.py      # Rules and win detection
│── gui.py             # Graphical user interface
│── main.py            # Main launcher

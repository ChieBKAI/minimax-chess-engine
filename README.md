# Chess Game with Minimax Algorithm Engine
This project provides an overview and guidance for implementing a simple chess game with a Minimax algorithm-based engine. The Minimax algorithm is a decision-making algorithm used in two-player games, such as chess, to find the optimal move for a player, assuming the opponent plays perfectly.

## Introduction
This project focuses on creating a chess game where the computer opponent uses the Minimax algorithm for decision-making. The Minimax algorithm evaluates possible future game states to determine the best move.

## Dependencies
- Python (>=3.6)
- Pygame library (for chess board visualization and interaction)

Install the required dependencies using:
```bash
pip install pygame
```

## Getting Started
Clone the repository:
```bash
git clone https://github.com/ChieBKAI/minimax-chess-engine.git
cd chess-game-minimax
```

## Minimax Algorithm Overview
The Minimax algorithm is a decision-making algorithm commonly used in two-player games with perfect information, like chess. It explores the game tree, considering all possible moves and opponent responses, to find the best move for the current player.

The algorithm minimizes the possible loss for a worst-case scenario (hence "min") while assuming the opponent maximizes their advantage (hence "max").

![](https://i.imgur.com/HjFjdGO.png)

## Implementation
The implementation is organized into modules:

- ChessMain.py: Defines user interface.
- ChessEngine.py: Defines the chess game logic. 
- ChienKoNgu.py (*my fun name*): Implements the Minimax algorithm for the computer opponent.

## Game play
- Press 'z' to Undo move
- Press 'r' to reset the board to begin state
- Press 'e' to play as white side
- Press 'q' to play as black side
- Press 'z' or 'r' will disable the AI. If you want to play with AI after that, just press 'e' or 'q'.

![Game play](https://i.imgur.com/ebEvH57.png)

## References
[Creating a Chess Engine in Python](https://www.youtube.com/playlist?list=PLBwF487qi8MGU81nDGaeNE1EnNEPYWKY_)

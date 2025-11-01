# Checkers Game

A feature-rich Checkers variant built with Pygame. Supports Human vs Human, Human vs AI, and AI vs AI modes, dynamic board/window sizing, and Ludo-style stacking rules (pairs/triples) with stack-strength captures.

## Features

- Three modes:
  - Human vs Human
  - Human vs AI
  - AI vs AI
- Ludo-style stacking system:
  - Stack your own pieces up to 3 per square (pair/triple)
  - Move a single piece off a stack; remaining pieces stay
  - Visual stack indicator on the top piece (2 or 3)
- Stack-strength capture rules:
  - Singles capture singles
  - Pairs capture singles or pairs
  - Triples capture any stack
  - Captures remove the entire enemy stack at the jumped square
  - Multi-jumps supported if further captures are available
- Kings and promotion:
  - Pieces promote upon reaching the far edge (top for Red, bottom for White)
  - Kings move and capture diagonally in both directions
- Draw and stalemate handling (configurable):
  - Draw if too many moves without capture
  - Draw if the same position repeats multiple times
  - Stalemate: player with no valid moves loses
- UI/UX:
  - Green circles show valid moves
  - Yellow/Orange markers show the last move
  - Bottom info panel: turn, scores, and stacking hint
  - Menus to configure AI type, board size, and window size

## Installation

1) Activate your virtual environment (if using the bundled one):
```bash
pygame-env\Scripts\activate
```

2) Install dependencies if needed:
```bash
pip install -r requirements.txt
```

## How to Play

1) Run the game:
```bash
python main.py
```

2) From the menu:
- 1: Human vs Human
- 2: Human vs AI
- 3: AI vs AI
- 4: Configure AI (AI type, toggle stacking, toggle draw rules)
- 5: Change Board Size (6x6, 8x8, 10x10, 12x12)
- 6: Change Window Size (500–800)
- 7: Quit

3) Controls:
- Click a piece to select it
- Click a highlighted square to move (or to stack on a friendly piece)
- R: Restart current game
- M: Return to main menu

## Game Rules (as implemented)

- Movement:
  - Non-king pieces move 1 square diagonally forward onto empty squares
  - Moving onto a friendly piece stacks it (max 3 per square)
  - Only the top piece of a stack can move; moving it “breaks” the stack
- Captures (jumping):
  - Captures are standard diagonal jumps: over an adjacent enemy stack onto the empty square immediately beyond
  - A capture is only legal if attacker_stack_size ≥ defender_stack_size
  - The entire defender stack at the jumped square is removed
  - Multi-jumps are allowed; the stack size of the attacker stays constant during the sequence
  - If any capture is available for a selected piece, only capture moves for that piece are shown (the board prioritizes captures in get_valid_moves)
- Kings:
  - Promote upon reaching the last rank
  - Move and capture diagonally in both forward and backward directions
- End conditions:
  - Stalemate: current player has no valid moves → that player loses
  - Draw: configurable rules
    - Too many moves without capture
    - Position repetition

## Configuration

All core configuration lives in `constants.py`:
- Board size: `ROWS`, `COLS` (defaults 8x8; menu available to change at runtime)
- Window size: `BOARD_HEIGHT` (square board), `INFO_PANEL_HEIGHT`
- Draw rules:
  - `MAX_MOVES_WITHOUT_CAPTURE`
  - `MAX_POSITION_REPEATS`
  - `DRAW_RULES_ENABLED` (toggle on/off)
- Stacking rule toggle: `STACKING_ENABLED` (menu toggle provided)
- AI type selection defaults: `AI_PLAYER1_TYPE`, `AI_PLAYER2_TYPE`

## AI

- Original AI (minimax with alpha-beta) in `ai_player.py`
  - Stack-aware evaluation (counts pieces, stack size bonuses, center/advancement, etc.)
  - Move ordering prioritizes captures, then stacking moves, then normal moves
  - Adjustable depth (default set in `main.py`)
- Additional AI agents (optional) in `ai_agents.py`:
  - FuzzyMinimaxAgent
  - HeuristicBacktrackAgent
- Choose AI types in the “Configure AI” menu; each side can use a different agent

## File Overview

- `main.py`: Window, menus, runtime configuration, game loop, AI routing
- `game.py`: Game state, turn handling, UI overlays, draw/stalemate checks
- `board.py`: Board model, stacking and capture logic, move generation, evaluation
- `piece.py`: Piece rendering (with stack size badge)
- `ai_player.py`: Original AI (minimax + alpha-beta, move ordering)
- `ai_agents.py` (optional): Alternative AI agents (fuzzy/heuristic)
- `compare_agents.py` (optional): Utilities to compare AI agents
- `constants.py`: Sizes, colors, rules, defaults, and AI type constants
- `requirements.txt`: Python dependencies

## Notes

- Stacking is capped at 3 per square. Triples are very strong: only other triples can capture them.
- During multi-jumps, the attacker’s effective stack size stays the same for the entire sequence.
- Draw rules and stacking can be toggled in the AI configuration menu.

Enjoy playing Checkers! 🎮


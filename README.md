# Checkers Game

A full-featured Checkers game built with Pygame, supporting multiple game modes including AI vs AI, Human vs AI, and Human vs Human.

## Features

- **Three Game Modes:**
  - Human vs Human - Play against another person
  - Human vs AI - Challenge the computer
  - AI vs AI - Watch two AI players compete

- **Smart AI Player:**
  - Uses Minimax algorithm with alpha-beta pruning
  - Adjustable difficulty (search depth)
  - Evaluates board positions strategically

- **Complete Checkers Rules:**
  - Standard 8x8 board with 12 pieces per side
  - Piece promotion to kings when reaching opposite end
  - Mandatory captures
  - Kings can move in all directions
  - Multiple jumps in single turn

- **Beautiful UI:**
  - Classic checkerboard design
  - Smooth piece animations
  - Visual indicators for valid moves (green circles)
  - Real-time score display
  - Turn indicators

## Installation

1. Make sure you're in the pygame virtual environment:
   ```bash
   pygame-env\Scripts\activate
   ```

2. Verify pygame is installed:
   ```bash
   python -c "import pygame; print(pygame.ver)"
   ```

## How to Play

1. Run the game:
   ```bash
   python main.py
   ```

2. Select a game mode from the menu:
   - Press **1** for Human vs Human
   - Press **2** for Human vs AI
   - Press **3** for AI vs AI
   - Press **4** to Quit

3. Game Controls:
   - **Click** on a piece to select it
   - **Click** on a highlighted square to move
   - **R** - Restart the current game
   - **M** - Return to main menu

## Game Rules

- **Red pieces** start at the bottom and move upward
- **White pieces** start at the top and move downward
- Regular pieces can only move diagonally forward
- **Kings** (crowned pieces) can move diagonally in all directions
- You must capture opponent pieces when possible
- Capture by jumping over opponent's piece
- Multiple captures can be made in one turn
- Game ends when one player has no pieces left

## Files Structure

- `main.py` - Main game loop and menu system
- `game.py` - Game logic and state management
- `board.py` - Board representation and move validation
- `piece.py` - Piece class with rendering
- `ai_player.py` - AI implementation with minimax algorithm
- `constants.py` - Game constants and configurations

## AI Difficulty

The AI uses a minimax algorithm with alpha-beta pruning. You can adjust the AI difficulty by modifying the `ai_depth` parameter in `main.py`:

- `ai_depth = 2` - Easy (faster, less strategic)
- `ai_depth = 3` - Medium (default, balanced)
- `ai_depth = 4` - Hard (slower, more strategic)
- `ai_depth = 5+` - Very Hard (may be slow)

## Technical Details

- **Language:** Python 3.11
- **Framework:** Pygame 2.6.1
- **Resolution:** 800x900 pixels
- **AI Algorithm:** Minimax with Alpha-Beta Pruning
- **Board Evaluation:** Piece count + King bonus

## Credits

Created for the AI_project using Pygame framework.

Enjoy playing Checkers! 🎮


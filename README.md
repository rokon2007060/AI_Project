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

- **Unique Ludo-Style Stacking System:**
  - Create pairs and triples by stacking your own pieces (max 3)
  - Stack strength matters: Pairs can only be captured by pairs or triples
  - Triples can only be captured by other triples
  - Strategic depth: Build defenses or break stacks for mobility

- **Complete Checkers Rules:**
  - Standard 8x8 board with 12 pieces per side
  - Piece promotion to kings when reaching opposite end
  - Stack-based captures (strength matters!)
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
   - **Click** on a highlighted square to move (or stack on friendly piece)
   - **R** - Restart the current game
   - **M** - Return to main menu
   
4. See `STACKING_RULES.md` for detailed stacking strategy and rules

## Game Rules

### Basic Movement
- **Red pieces** start at the bottom and move upward
- **White pieces** start at the top and move downward
- Regular pieces can only move diagonally forward
- **Kings** (crowned pieces) can move diagonally in all directions

### Stacking System (NEW!)
- **Create stacks** by moving your pieces onto friendly pieces
- **Maximum stack size:** 3 pieces per square
- **Visual indicator:** Stack size shown as number on piece (2 or 3)
- **Breaking stacks:** Move a piece from any stack to separate it

### Capture Rules (Stack Strength)
- **Single pieces** can only capture other single pieces
- **Pairs (2 pieces)** can capture singles or pairs
- **Triples (3 pieces)** can capture any stack
- **Entire stacks** are captured and removed together
- Multiple captures can be made in one turn

### Victory Conditions
- Game ends when one player has no pieces left
- Stalemate: Player with no valid moves loses
- Draw: 40 moves without capture or position repeats 3 times

## Files Structure

- `main.py` - Main game loop and menu system
- `game.py` - Game logic and state management
- `board.py` - Board representation and move validation (with stacking)
- `piece.py` - Piece class with rendering (stack visualization)
- `ai_player.py` - AI implementation with minimax algorithm
- `constants.py` - Game constants and configurations
- `STACKING_RULES.md` - Detailed stacking rules documentation
- `STACKING_IMPLEMENTATION.md` - Technical implementation details

## AI Difficulty

The AI uses a minimax algorithm with alpha-beta pruning. You can adjust the AI difficulty by modifying the `ai_depth` parameter in `main.py`:

- `ai_depth = 2` - Easy (faster, less strategic)
- `ai_depth = 3` - Medium (default, balanced)
- `ai_depth = 4` - Hard (slower, more strategic)
- `ai_depth = 5+` - Very Hard (may be slow)

## Technical Details

- **Language:** Python 3.11
- **Framework:** Pygame 2.6.1
- **Resolution:** Adjustable (500-800 pixels)
- **AI Algorithm:** Minimax with Alpha-Beta Pruning
- **Board Evaluation:** Piece count + King bonus + Stack formation bonus
- **Data Structure:** List-based stacking system (max 3 pieces per cell)

## Credits

Created for the AI_project using Pygame framework.

Enjoy playing Checkers! 🎮


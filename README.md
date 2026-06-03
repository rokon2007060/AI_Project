# Advanced Checkers Game with AI Agents

A sophisticated Checkers variant built with **Pygame**, featuring multiple **AI algorithms**, **Ludo-style stacking rules**, and comprehensive game configuration options. This project demonstrates advanced AI techniques including minimax with alpha-beta pruning, fuzzy logic evaluation, and constraint satisfaction heuristics (MRV/LCV).

## 🎮 Overview

This is an educational AI project implementing a feature-rich Checkers game with configurable gameplay modes and multiple intelligent agents. The game supports Human vs Human, Human vs AI, and AI vs AI matches with flexible board sizing, window scaling, and rule customization.

### Key Features

- **Three Game Modes:**
  - Human vs Human (local multiplayer)
  - Human vs AI (single player vs intelligent opponent)
  - AI vs AI (watch two AI agents compete)

- **Advanced Stacking System (Ludo-style):**
  - Stack your own pieces up to 3 per square (pair/triple)
  - Move a single piece off a stack; remaining pieces stay in place
  - Visual stack strength indicator on the top piece (2 or 3)
  - Stack-aware capture mechanics with strength-based rules

- **Stack-Strength Capture Rules:**
  - Singles capture singles
  - Pairs capture singles or pairs
  - Triples capture any stack
  - Captures remove the entire enemy stack at the jumped square
  - Multi-jump sequences supported if further captures are available

- **King Promotion & Movement:**
  - Pieces promote upon reaching the far edge (top row for Red, bottom row for White)
  - Kings move and capture diagonally in both forward and backward directions

- **Draw & Stalemate Handling:**
  - Draw if too many moves without capture (configurable threshold)
  - Draw if the same position repeats multiple times (configurable limit)
  - Stalemate: player with no valid moves loses

- **Dynamic UI/UX:**
  - Green circles show valid moves for selected piece
  - Yellow/Orange markers highlight the last move made
  - Bottom info panel displays: current turn, piece scores, and stacking hints
  - Intuitive menus for AI type selection, board size, and window size configuration

- **Multiple AI Strategies:**
  - **Original Minimax AI** (alpha-beta pruning, move ordering)
  - **Minimax + Backtracking** (MRV/LCV heuristics with roulette wheel selection)
  - **Minimax + Fuzzy Logic** (fuzzy evaluation metrics with roulette wheel selection)

## 📋 Project Structure

```
ai_project/
├── main.py                    # Entry point, menus, game loop, AI routing
├── game.py                    # Game state management, turn handling, UI overlays
├── board.py                   # Board model, stacking logic, move generation, evaluation
├── piece.py                   # Piece rendering with stack size badges
├── ai_player.py               # Original minimax AI with alpha-beta pruning
├── ai_agents.py               # Alternative AI agents (Backtrack, Fuzzy variants)
├── astar_capture.py           # A* algorithm utilities for capture planning
├── fuzzy_eval.py              # Fuzzy logic evaluation system
├── compare_agents.py           # Utilities to benchmark and compare AI agents
├── performance_logger.py       # Logging and stats collection
├── stack.py                   # Stack data structure utilities
├── constants.py               # Global configuration (colors, sizes, rules, AI settings)
├── requirements.txt           # Python dependencies (pygame==2.6.1)
├── report.tex                 # LaTeX technical report documentation
├── OPTIONAL_CAPTURE_CHANGES.md # Notes on optional capture rule variations
├── run_checkers.bat           # Windows batch script to launch game
├── run_checkers.ps1           # Windows PowerShell script to launch game
└── pygame-env/                # Virtual environment (bundled dependencies)
```

## 🛠️ Installation

### Prerequisites
- **Python 3.8+**
- **Pygame 2.6.1**

### Setup

#### Option 1: Using Bundled Virtual Environment (Windows)
```bash
# Activate the bundled virtual environment
pygame-env\Scripts\activate

# Install/update dependencies if needed
pip install -r requirements.txt

# Run the game
python main.py
```

#### Option 2: Manual Virtual Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# or (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

#### Option 3: Quick Launch (Windows Only)

```bash
# Using batch script
run_checkers.bat

# or using PowerShell
powershell -ExecutionPolicy Bypass -File run_checkers.ps1
```

## 🎯 How to Play

### Starting the Game
```bash
python main.py
```

### Main Menu Options
```
1. Human vs Human      - Play locally against another human
2. Human vs AI         - Play against an intelligent AI opponent
3. AI vs AI            - Watch two AI agents compete
4. Configure AI        - Select AI type, toggle stacking, configure draw rules
5. Change Board Size   - Select from 6x6, 8x8, 10x10, or 12x12
6. Change Window Size  - Adjust window height (500–800px)
7. Quit                - Exit the game
```

### In-Game Controls

| Control | Action |
|---------|--------|
| **Click piece** | Select a piece to move |
| **Click highlighted square** | Move to that square (or stack on friendly piece) |
| **R** | Restart current game |
| **M** | Return to main menu |
| **Drag/Click** | Interact with UI menus |

### Game Flow

1. **Piece Selection:** Click a piece to select it
2. **Valid Moves Display:** Green circles show all legal moves for the selected piece
3. **Move Execution:** Click a highlighted square to move (or to stack on a friendly piece)
4. **Stack Indicator:** The number badge on top pieces shows stack size (2 or 3)
5. **Last Move Tracking:** Yellow/Orange markers indicate the previous move
6. **Win Condition:** Eliminate all opponent pieces or force them into stalemate

## 🧠 AI Configuration Menu

### AI Type Selection

**Red Player (Player 1) Options:**
- 1: **Original Minimax** - Classic alpha-beta pruning (fast, reliable)
- 2: **Minimax + Backtracking** - Uses MRV/LCV constraint satisfaction with roulette wheel
- 3: **Minimax + Fuzzy Logic** - Uses fuzzy logic evaluation with roulette wheel

**White Player (Player 2) Options:**
- 4: **Original Minimax**
- 5: **Minimax + Backtracking**
- 6: **Minimax + Fuzzy Logic**

### Additional Configuration
- **7: Stacking Toggle** - Enable/disable Ludo-style stacking (ON/OFF)
- **8: Draw Rules Toggle** - Enable/disable draw conditions (ON/OFF or "Fight to Win!" mode)

## 📐 Game Rules (Implementation Details)

### Movement
- **Non-king pieces** move 1 square diagonally forward onto empty squares
- **Moving onto a friendly piece** stacks it (maximum 3 per square)
- **Only the top piece** of a stack can move; moving it "breaks" the stack
- **Kings** can move diagonally in both forward and backward directions

### Captures (Jumping)
- **Standard diagonal jumps:** Over an adjacent enemy stack onto the empty square immediately beyond
- **Legal capture condition:** `attacker_stack_size ≥ defender_stack_size`
- **Capture effect:** The entire defender stack at the jumped square is removed
- **Multi-jumps:** Allowed; the attacker's stack size remains constant throughout the sequence
- **Capture prioritization:** If any capture is available for a selected piece, only capture moves are shown

### Kings
- **Promotion:** Pieces promote when reaching the last rank (top for Red, bottom for White)
- **Movement:** Can move and capture diagonally in both forward and backward directions

### End Conditions
1. **Stalemate:** Current player has no valid moves → that player loses
2. **Draw (if enabled):**
   - Too many moves without capture (configurable: `MAX_MOVES_WITHOUT_CAPTURE`)
   - Position repetition (configurable: `MAX_POSITION_REPEATS`)

## ⚙️ Configuration

### Core Settings (`constants.py`)

| Setting | Description | Default |
|---------|-------------|---------|
| `ROWS`, `COLS` | Board dimensions | 8, 8 |
| `BOARD_HEIGHT` | Board pixel height (square) | 800 |
| `INFO_PANEL_HEIGHT` | Bottom panel height (pixels) | 120 |
| `MAX_MOVES_WITHOUT_CAPTURE` | Moves before draw (if enabled) | 60 |
| `MAX_POSITION_REPEATS` | Position repetitions before draw (if enabled) | 3 |
| `DRAW_RULES_ENABLED` | Enable draw conditions | True |
| `STACKING_ENABLED` | Enable Ludo-style stacking | True |
| `AI_PLAYER1_TYPE` | Red player AI type | `AI_TYPE_ORIGINAL` |
| `AI_PLAYER2_TYPE` | White player AI type | `AI_TYPE_ORIGINAL` |
| `AI_DEPTH_FUZZY` | Fuzzy AI search depth | 4 |
| `AI_DEPTH_BACKTRACK` | Backtrack AI search depth | 4 |

### Available Constants

```python
# Game modes
HUMAN_VS_HUMAN = 0
HUMAN_VS_AI = 1
AI_VS_AI = 2

# AI types
AI_TYPE_ORIGINAL = 0
AI_TYPE_MINIMAX_BACKTRACK = 1
AI_TYPE_MINIMAX_FUZZY = 2

# Colors
RED, WHITE, BLACK, GOLD, GREEN, YELLOW, ORANGE, LIGHT_BLUE, BLUE

# Board sizes (menu options)
6x6, 8x8, 10x10, 12x12

# Window sizes (menu options)
500x620, 600x720, 700x820, 800x920
```

## 🤖 AI Algorithms

### 1. **Original Minimax AI** (`ai_player.py`)
- **Algorithm:** Minimax with alpha-beta pruning
- **Move Ordering:** 
  - Capture moves prioritized
  - Stacking moves prioritized
  - Normal moves last
- **Evaluation Function:**
  - Piece count (higher is better)
  - Stack size bonuses (pairs & triples worth more)
  - Center control bonus
  - Advancement bonus (pieces closer to promotion)
  - King presence bonus
- **Depth:** Configurable (default: 4)
- **Performance:** Fast, suitable for larger boards

### 2. **Minimax + Backtracking AI** (`ai_agents.py`)
- **Algorithm:** Minimax with constraint satisfaction heuristics
- **Heuristics:** MRV (Minimum Remaining Values) and LCV (Least Constraining Value)
- **Move Selection:** Roulette wheel selection (probabilistic, not deterministic)
- **Evaluation:** Same as Original Minimax
- **Depth:** Configurable (default: 4)
- **Use Case:** More analytical, explores different strategic branches

### 3. **Minimax + Fuzzy Logic AI** (`ai_agents.py` + `fuzzy_eval.py`)
- **Algorithm:** Minimax with fuzzy logic evaluation
- **Fuzzy Metrics:**
  - Piece count fuzzy evaluation
  - Stack strength assessment
  - Board control evaluation
  - Advancement scoring
- **Move Selection:** Roulette wheel (probabilistic)
- **Evaluation:** Combines fuzzy membership functions for nuanced position assessment
- **Depth:** Configurable (default: 4)
- **Use Case:** More unpredictable, interesting for varied gameplay

### Performance Logging
Each AI agent logs detailed statistics after each move:
- Number of nodes expanded
- Strategy used
- Computation time (seconds)
- Move information

Access logs via console output when AI moves are made.

## 📊 File Descriptions

| File | Purpose | Key Functions |
|------|---------|---------------|
| **main.py** | Game initialization, menus, event loop | Window management, menu drawing, game mode routing |
| **game.py** | Game state, turn management, UI | Board updates, winner detection, stalemate/draw checks |
| **board.py** | Board model, move generation, capture logic | Move validation, stack operations, board evaluation |
| **piece.py** | Piece rendering and drawing | Visual representation with stack badges |
| **ai_player.py** | Original minimax with alpha-beta pruning | `get_best_move()`, evaluation function |
| **ai_agents.py** | Alternative AI implementations | `MinimaxBacktrackAgent`, `MinimaxFuzzyAgent`, `FuzzyMinimaxAgent`, `HeuristicBacktrackAgent` |
| **astar_capture.py** | A* utilities for capture sequence planning | Optional capture optimization |
| **fuzzy_eval.py** | Fuzzy logic evaluation system | Fuzzy membership functions, evaluation metrics |
| **compare_agents.py** | Benchmarking and comparison utilities | Testing different AI agents against each other |
| **performance_logger.py** | Performance metrics and statistics | Logging, timing, node counting |
| **stack.py** | Stack data structure | Piece stacking operations |
| **constants.py** | Global configuration and constants | Colors, sizes, rules, AI settings, board dimensions |
| **report.tex** | Technical documentation (LaTeX) | Detailed algorithm descriptions, testing results |

## 🔧 Advanced Usage

### Comparing AI Agents
Use `compare_agents.py` to run benchmarking tests:
```bash
python compare_agents.py
```

### Analyzing Performance
Monitor console output for AI statistics:
- Nodes expanded per move
- Search strategy used
- Computation time
- Move quality metrics

### Custom AI Development
Extend `ai_agents.py` to create new AI algorithms:
```python
class CustomAgent:
    def __init__(self, color, depth=4):
        self.color = color
        self.depth = depth
    
    def get_move(self, board, game):
        # Implement your algorithm
        return new_board, move_info, was_capture
```

### Adjusting Difficulty
Modify AI depth in `constants.py`:
```python
AI_DEPTH_FUZZY = 3        # Easier (less lookahead)
AI_DEPTH_BACKTRACK = 5    # Harder (more lookahead)
```

## 📝 Notes

- **Stacking Limits:** Pieces are capped at 3 per square. Triples are the strongest: only other triples can capture them
- **Multi-Jump Mechanics:** During multi-jumps, the attacker's effective stack size remains constant for the entire sequence
- **Configuration Persistence:** AI type and rule settings are maintained across games in the same session
- **Draw Rules:** Can be toggled in AI configuration menu; "Fight to Win" mode disables draws entirely
- **Board Scaling:** Larger boards (10x10, 12x12) require more window space; use window size menu to adjust
- **Virtual Environment:** Use bundled `pygame-env` for consistent dependency management

## 📚 Dependencies

- **pygame==2.6.1** - Game rendering and event handling
- Python standard library modules (sys, time, threading, etc.)

## 📖 Technical Documentation

See `report.tex` for comprehensive technical documentation including:
- Algorithm analysis and complexity
- Evaluation function details
- Performance benchmarks
- Implementation notes
- Future improvements

## 🚀 Performance Tips

1. **Smaller Boards** for faster AI decisions (6x6 or 8x8)
2. **Lower AI Depth** for quicker games (`AI_DEPTH_FUZZY = 3`)
3. **Disable Draw Rules** for continuous gameplay
4. **Use Original Minimax** for fastest performance
5. **Monitor Console** for AI statistics and optimization opportunities

## 🎓 Educational Value

This project demonstrates:
- **Minimax Algorithm** with alpha-beta pruning
- **Constraint Satisfaction** (MRV/LCV heuristics)
- **Fuzzy Logic** application in game AI
- **Game State Management** and UI design
- **Performance Optimization** techniques
- **Software Architecture** and modularity

## 📄 License

This project is provided as-is for educational purposes.

## 🔗 Additional Resources

- Pygame Documentation: https://www.pygame.org/docs/
- Minimax Algorithm: https://en.wikipedia.org/wiki/Minimax
- Alpha-Beta Pruning: https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
- Fuzzy Logic: https://en.wikipedia.org/wiki/Fuzzy_logic

---

**Enjoy playing Advanced Checkers!** 🎮♟️

For issues, improvements, or contributions, please refer to the technical report and code documentation.

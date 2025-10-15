# Checkers Game - Complete Usage Guide

## Quick Start

### Method 1: Double-click the batch file (Easiest)
Simply double-click `run_checkers.bat` in the file explorer.

### Method 2: PowerShell
```powershell
.\run_checkers.ps1
```

### Method 3: Manual activation
```bash
# Activate the virtual environment
.\pygame-env\Scripts\activate

# Run the game
python main.py
```

## Game Modes

### 1. Human vs Human
- Two players take turns on the same computer
- Red player goes first (bottom pieces)
- White player goes second (top pieces)
- Click on your pieces to select and move them

### 2. Human vs AI
- You play as Red (bottom pieces) against the computer
- The AI plays as White (top pieces)
- The AI will think for a few seconds before making its move
- Window title shows "AI Thinking..." when the computer is calculating

### 3. AI vs AI
- Watch two AI players compete against each other
- Great for learning strategies
- Both players use the same AI algorithm
- You can press 'R' to restart and see different game outcomes

## Controls

### Mouse Controls
- **Left Click on Piece**: Select one of your pieces
- **Left Click on Green Circle**: Move selected piece to that position
- **Left Click on Menu Option**: Select game mode in menu

### Keyboard Controls
- **R Key**: Restart the current game (keeps same game mode)
- **M Key**: Return to main menu (change game mode)
- **1 Key**: (In menu) Start Human vs Human
- **2 Key**: (In menu) Start Human vs AI
- **3 Key**: (In menu) Start AI vs AI
- **4 Key**: (In menu) Quit game

## Game Rules

### Basic Movement
1. **Regular Pieces** (Red/White circles):
   - Move diagonally forward only
   - Can only move to adjacent dark squares
   - Must capture opponent pieces when possible

2. **Kings** (Pieces with crown ♔):
   - Created when a piece reaches the opposite end of the board
   - Can move diagonally in ALL directions (forward and backward)
   - More powerful and strategic

### Capturing
- Jump over an opponent's piece to capture it
- You can make multiple jumps in one turn
- If a capture is available, you MUST take it
- Captured pieces are removed from the board

### Winning
- Eliminate all opponent pieces
- The game displays "RED WINS!" or "WHITE WINS!" when someone wins
- Score is shown at the bottom: "Red: X White: Y"

## Visual Guide

### Board Colors
- **Light Brown squares**: Can't move here
- **Dark Brown squares**: Valid board positions
- **Green circles**: Valid moves for selected piece
- **Red pieces**: Player 1 (Human in Human vs AI mode)
- **White pieces**: Player 2 (AI in Human vs AI mode)

### Screen Layout
```
┌─────────────────────────┐
│                         │
│    8x8 Checkerboard     │
│                         │
│    (800x800 pixels)     │
│                         │
└─────────────────────────┘
┌─────────────────────────┐
│ Turn Info & Score       │
│ Red: 12  White: 12      │
└─────────────────────────┘
```

## Tips & Strategies

### For Beginners
1. **Protect your back row**: Don't move these pieces early - they prevent opponent from getting kings
2. **Make kings**: Try to get your pieces to the opposite end
3. **Control the center**: Central pieces have more movement options
4. **Force captures**: Sometimes you can force opponent into bad captures

### Against AI
1. **Think ahead**: The AI looks 3 moves ahead, try to plan your moves
2. **Trade wisely**: Only trade pieces when it benefits you
3. **Use kings effectively**: Kings are much more valuable than regular pieces
4. **Corner control**: Corner pieces are harder to capture

### Watching AI vs AI
- Observe common strategies
- Notice how AI values kings (worth 1.5 regular pieces)
- Learn opening moves and endgame techniques
- Each game is different due to move evaluation

## Troubleshooting

### Game won't start
1. Make sure pygame is installed: `pip install pygame`
2. Verify Python 3.11 is installed
3. Check that you're in the pygame-env virtual environment

### Game is slow / AI takes too long
- The AI thinks for 2-5 seconds on medium difficulty
- This is normal - it's calculating the best move
- If too slow, you can reduce AI difficulty in `main.py` (change `ai_depth = 3` to `ai_depth = 2`)

### Window doesn't respond
- Wait for AI to finish thinking
- Check if the game window has focus (click on it)
- Press 'R' to restart if stuck

### Can't click pieces
- Make sure it's your turn (check turn indicator)
- Only pieces of the current player can be selected
- In AI vs AI mode, you can't click pieces (just watch)

## Customization

### Adjusting AI Difficulty
Edit `main.py` and find this line:
```python
ai_depth = 3  # Change this number
```

- `ai_depth = 2`: Easy (faster, makes more mistakes)
- `ai_depth = 3`: Medium (default, balanced)
- `ai_depth = 4`: Hard (slower, smarter)
- `ai_depth = 5`: Expert (very slow, best moves)

### Changing Colors
Edit `constants.py` to customize colors:
```python
PLAYER1_COLOR = RED      # Red pieces
PLAYER2_COLOR = WHITE    # White pieces
LIGHT_BROWN = (240, 217, 181)  # Light squares
DARK_BROWN = (181, 136, 99)    # Dark squares
```

### Window Size
Edit `constants.py`:
```python
WIDTH, HEIGHT = 800, 900  # Change these values
```

## Technical Information

### System Requirements
- **OS**: Windows 10/11 (or Mac/Linux with minor adjustments)
- **Python**: 3.11+
- **RAM**: 512 MB minimum
- **Display**: 800x900 minimum resolution

### Performance
- **FPS**: Locked at 60 frames per second
- **AI Speed**: 1-5 seconds per move (depending on difficulty)
- **Memory**: ~50-100 MB RAM usage

### File Structure
```
AI_project/
├── main.py              # Entry point, menu, game loop
├── game.py              # Game state management
├── board.py             # Board logic and move validation
├── piece.py             # Piece rendering and properties
├── ai_player.py         # Minimax AI algorithm
├── constants.py         # Configuration and colors
├── README.md            # Project overview
├── USAGE_GUIDE.md       # This file
├── requirements.txt     # Python dependencies
├── run_checkers.bat     # Windows launcher
├── run_checkers.ps1     # PowerShell launcher
└── pygame-env/          # Virtual environment
```

## Frequently Asked Questions

**Q: Can I play online with friends?**
A: Not currently - this version is local multiplayer only.

**Q: Can I save my game progress?**
A: Not yet, but you can add this feature by modifying the code.

**Q: Why does the AI sometimes seem to make mistakes?**
A: The AI is limited by search depth. Higher depth = smarter AI but slower.

**Q: Can I make the board bigger?**
A: Yes! Edit `ROWS, COLS` in `constants.py` (but standard checkers uses 8x8).

**Q: The game is too easy/hard**
A: Adjust `ai_depth` in `main.py` (line ~44 in game_loop function).

## Credits

Built with:
- Python 3.11
- Pygame 2.6.1
- Minimax algorithm with Alpha-Beta pruning

Created for E:\AI_project

---

**Enjoy playing Checkers!** 🎮♟️

For bugs or feature requests, check the code in the respective .py files.


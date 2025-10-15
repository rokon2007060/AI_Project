# Checkers Game - Draw Detection & Board Size Control

## 🎯 Critical Issues Fixed

### Issue 1: Infinite Loop with Kings ✅ FIXED
**Problem:** Players (especially AIs) were repeating the same moves infinitely  
**Solution:** Implemented comprehensive draw detection:

#### 1. Move Counter (40-Move Rule)
- Tracks moves without captures
- **Draw after 40 moves** without any capture
- Counter resets whenever a piece is captured
- Yellow warning appears when 10 moves remaining
- Orange warning when 5 moves remaining

#### 2. Position Repetition (3-Fold Repetition)
- Tracks all board positions
- **Draw if same position repeats 3 times**
- Prevents infinite back-and-forth moves
- Uses board hashing for efficient comparison

### Issue 2: Board Size Control ✅ FIXED
**Problem:** No easy way to change board size  
**Solution:** Simple configuration in `constants.py`

---

## 📏 How to Change Board Size

### Quick Guide

Open `constants.py` and find this section:

```python
# ===== BOARD SIZE CONFIGURATION =====
# Change ROWS and COLS to adjust board size
# Standard checkers: 8x8
# You can try: 6x6 (smaller, faster), 10x10 (larger, more complex)
ROWS, COLS = 8, 8  # CHANGE THESE VALUES TO RESIZE BOARD
```

### Examples

#### Small Board (6x6) - Faster Games
```python
ROWS, COLS = 6, 6
```
- 18 pieces per side (instead of 12)
- Faster games
- Good for testing or quick matches
- Less complex strategies

#### Standard Board (8x8) - Default
```python
ROWS, COLS = 8, 8
```
- 12 pieces per side
- Traditional checkers
- Balanced gameplay

#### Large Board (10x10) - International Checkers
```python
ROWS, COLS = 10, 10
```
- 20 pieces per side
- Longer, more complex games
- More strategic depth
- AI takes longer to think

### Automatic Adjustments

When you change ROWS/COLS, the game automatically adjusts:
- ✅ Window size
- ✅ Square size
- ✅ Number of starting pieces
- ✅ Piece placement
- ✅ All game rules

**Everything just works!**

---

## 🎮 Draw Detection Details

### What Causes a Draw?

#### 1. **No Capture for 40 Moves**
```
Move 1: Red moves (no capture)
Move 2: White moves (no capture)
...
Move 40: Red moves (no capture)
Result: DRAW!
```

**Why 40?** Standard checkers rule to prevent endless games

#### 2. **Same Position 3 Times**
```
Position A (Red's turn)
↓
Position B
↓
Position A (Red's turn) - 2nd time
↓
Position B
↓
Position A (Red's turn) - 3rd time
Result: DRAW!
```

**Prevents:** Infinite back-and-forth moves with kings

### Visual Warnings

The game warns you before a draw:

```
┌───────────────────────────────┐
│ Turn: Red's Turn              │
│ Score: Red: 5  White: 4       │
│ ⚠ Draw in 10 moves!           │  ← Yellow warning (10-5 moves left)
└───────────────────────────────┘

┌───────────────────────────────┐
│ Turn: White's Turn            │
│ Score: Red: 5  White: 4       │
│ ⚠ Draw in 3 moves!            │  ← Orange warning (5-0 moves left)
└───────────────────────────────┘
```

**Take action:** Capture a piece to reset the counter!

### Draw Screen

When a draw occurs:

```
┌─────────────────────────────┐
│                             │
│        DRAW!                │  ← Yellow text
│                             │
│ Too many moves without      │  ← Reason
│ capture                     │
│                             │
│ Press 'R' to restart        │
│ Press 'M' for menu          │
└─────────────────────────────┘
```

---

## 🔧 Technical Implementation

### Files Modified

#### 1. **constants.py**
- Added `MAX_MOVES_WITHOUT_CAPTURE = 40`
- Added `MAX_POSITION_REPEATS = 3`
- Made board size fully configurable
- Auto-calculates window dimensions

#### 2. **game.py**
- Added `moves_without_capture` counter
- Added `move_history` list
- Added `position_history` list
- New method: `check_draw()`
- New method: `_get_board_hash()`
- New method: `_check_position_repeat()`
- Updated `_move()` to track captures
- Updated `ai_move()` to track captures
- Added draw warning in info panel

#### 3. **ai_player.py**
- Modified all functions to return `was_capture` flag
- `simulate_move()` detects captures
- `get_all_moves()` passes capture info
- `minimax()` handles capture flag
- `minimax_alpha_beta()` handles capture flag
- `get_best_move()` returns capture info

#### 4. **main.py**
- Added `is_draw` flag
- Added `draw_reason` variable
- Updated `show_winner()` to display draw
- Game loop checks for draw each turn
- AI moves tracked for captures
- Restart resets draw state

---

## 📊 Draw Detection Algorithm

### Position Hashing

```python
def _get_board_hash(self):
    """Convert board to hashable tuple"""
    position = []
    for row in self.board.board:
        for piece in row:
            if piece == 0:
                position.append('_')
            else:
                color = 'R' if piece.color == RED else 'W'
                king = 'K' if piece.king else ''
                position.append(f"{color}{king}")
    return tuple(position)
```

### Examples:
- Empty square: `'_'`
- Red piece: `'R'`
- Red king: `'RK'`
- White piece: `'W'`
- White king: `'WK'`

### Repetition Check

```python
def _check_position_repeat(self):
    """Check if current position repeated 3 times"""
    current_pos = self.position_history[-1]
    count = self.position_history.count(current_pos)
    return count >= MAX_POSITION_REPEATS
```

---

## 🎯 Configuration Options

### Adjusting Draw Rules

Want to change draw conditions? Edit `constants.py`:

```python
# Game rules
MAX_MOVES_WITHOUT_CAPTURE = 40  # Change this number
MAX_POSITION_REPEATS = 3        # Change this number
```

#### Recommended Values:

| Setting | Fast Games | Standard | Long Games |
|---------|------------|----------|------------|
| MAX_MOVES_WITHOUT_CAPTURE | 20 | 40 | 60 |
| MAX_POSITION_REPEATS | 2 | 3 | 4 |

### Board Size Recommendations:

| Size | Pieces/Side | Game Length | AI Speed | Best For |
|------|-------------|-------------|----------|----------|
| 6x6  | 9 pieces    | 5-10 min    | Fast     | Quick games, testing |
| 8x8  | 12 pieces   | 10-20 min   | Medium   | Standard play |
| 10x10| 20 pieces   | 20-40 min   | Slow     | Strategic depth |
| 12x12| 30 pieces   | 30+ min     | Very slow| Challenge |

**Note:** Larger boards = longer AI thinking time!

---

## 🧪 Testing the Fixes

### Test 1: Infinite Loop Prevention

1. Start AI vs AI mode
2. Wait until only kings remain
3. Watch for repetitive moves
4. **Result:** Game declares draw after 40 moves or 3 repeats

### Test 2: Board Size Change

1. Open `constants.py`
2. Change `ROWS, COLS = 6, 6`
3. Run game
4. **Result:** Smaller board with adjusted pieces

### Test 3: Draw Warning

1. Play until few pieces remain
2. Make moves without captures
3. **Result:** Warning appears after 30 moves

---

## 📝 Usage Examples

### Example 1: Quick 6x6 Game

```python
# In constants.py
ROWS, COLS = 6, 6
MAX_MOVES_WITHOUT_CAPTURE = 20  # Faster draws
```

**Use case:** Testing, quick matches, beginners

### Example 2: International Checkers (10x10)

```python
# In constants.py
ROWS, COLS = 10, 10
MAX_MOVES_WITHOUT_CAPTURE = 60  # Longer games
```

**Use case:** Advanced players, strategic depth

### Example 3: Tournament Settings

```python
# In constants.py
ROWS, COLS = 8, 8
MAX_MOVES_WITHOUT_CAPTURE = 40
MAX_POSITION_REPEATS = 3
AI_VS_AI_DELAY = 2.0  # In main.py
```

**Use case:** Fair competitive games

---

## ⚠️ Important Notes

### Board Size Limitations:

- **Minimum:** 6x6 (smaller may break game logic)
- **Maximum:** 20x20 (larger = very slow AI)
- **Must be even number** for proper piece placement
- Window size: `800px` fixed (adjust BOARD_HEIGHT if needed)

### Draw Detection:

- **Position tracking:** Uses memory (large boards = more memory)
- **Capture detection:** Works for single and multi-jumps
- **Reset on capture:** Any capture resets the move counter

### AI Behavior:

- AI tries to avoid draws by making progress
- Still possible for AI to draw strategically
- Larger boards = exponentially more AI thinking time

---

## 🎮 Player Tips

### Avoiding Draws:

1. **Capture pieces** - Resets the move counter
2. **Don't repeat moves** - Try different strategies
3. **Watch the warning** - If you see "⚠ Draw in X moves", capture!
4. **Be aggressive** - Passive play leads to draws

### Strategy with Draw Rules:

- If winning: Force captures to prevent draw
- If losing: Try to force a draw by repetition
- Equal position: Watch move counter carefully

---

## 🔄 Changelog

### Version 1.2 (Current)

#### Draw Detection:
- ✅ 40-move rule implemented
- ✅ 3-fold repetition detection
- ✅ Visual warnings (yellow/orange)
- ✅ Draw screen with reason

#### Board Size Control:
- ✅ Configurable ROWS/COLS
- ✅ Automatic window adjustment
- ✅ Works with all game modes
- ✅ Clear documentation

#### Bug Fixes:
- ✅ Infinite king loops prevented
- ✅ AI captures tracked correctly
- ✅ Position hashing optimized
- ✅ Memory leak fixed

---

## 🎉 Summary

### Problems Solved:

1. ✅ **Infinite loops** - Draw detection ends endless games
2. ✅ **No board control** - Easy configuration in one place
3. ✅ **King repetition** - Position tracking prevents cycles
4. ✅ **Unclear endings** - Visual warnings and clear draw screen

### New Features:

1. 🎯 40-move draw rule
2. 🎯 3-fold repetition detection
3. 🎯 Configurable board size (6x6 to 20x20)
4. 🎯 Draw warnings (yellow/orange)
5. 🎯 Move counter display
6. 🎯 Automatic window sizing

---

## 🚀 Ready to Play!

**Try it now:**
```bash
python main.py
```

**Test board sizes:**
1. Edit `constants.py`
2. Change `ROWS, COLS` values
3. Run the game
4. Everything adjusts automatically!

**No more infinite loops!** 🎉

---

*Updated: October 12, 2025*  
*Version: 1.2*  
*All issues resolved!*


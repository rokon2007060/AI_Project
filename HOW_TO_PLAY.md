# 🎮 Checkers Game - How to Play

## 🚀 Quick Start (3 Easy Steps)

### Step 1: Launch the Game
**Easiest Method:** Double-click `run_checkers.bat`

**Alternative Methods:**
```bash
# Method 2: Using Python directly
cd E:\AI_project
.\pygame-env\Scripts\activate
python main.py

# Method 3: Using PowerShell script
.\run_checkers.ps1
```

### Step 2: Choose Game Mode
When the menu appears, press:
- **1** for Human vs Human (play with a friend)
- **2** for Human vs AI (challenge the computer)
- **3** for AI vs AI (watch computers play)
- **4** to Quit

### Step 3: Play!
- Click on your pieces to select them
- Click on green circles to move
- Have fun! 🎉

---

## 🎯 Detailed Instructions

### Main Menu
```
╔═══════════════════════════════╗
║      CHECKERS GAME           ║
╠═══════════════════════════════╣
║  1. Human vs Human           ║
║  2. Human vs AI              ║
║  3. AI vs AI                 ║
║  4. Quit                     ║
╚═══════════════════════════════╝
```

**How to Select:**
- Press number keys (1-4) on keyboard
- OR click directly on the option with mouse

---

## 🕹️ Game Controls

### Mouse Controls
| Action | How |
|--------|-----|
| Select piece | Left click on your piece |
| Move piece | Left click on green circle |
| Menu selection | Left click on menu option |

### Keyboard Shortcuts
| Key | Action |
|-----|--------|
| **R** | Restart current game |
| **M** | Return to main menu |
| **1** | Human vs Human (in menu) |
| **2** | Human vs AI (in menu) |
| **3** | AI vs AI (in menu) |
| **4** | Quit game (in menu) |

---

## 📖 Game Rules

### Basic Rules
1. **Red pieces** start at the bottom (rows 5-7)
2. **White pieces** start at the top (rows 0-2)
3. **Red always moves first**
4. Players alternate turns

### Movement Rules
| Piece Type | Movement |
|------------|----------|
| **Regular Piece** | Diagonal forward only |
| **King Piece (♔)** | Diagonal in all directions |

### Capturing
- Jump over opponent's piece diagonally
- Captured piece is removed from board
- **Multiple jumps** allowed in single turn
- **Must capture** if capture is available

### Becoming a King
- Reach the opposite end of the board
- Regular piece → King (gets crown ♔)
- Kings are more powerful!

### Winning
- **Capture all opponent pieces** = YOU WIN! 🏆
- Opponent has no valid moves = YOU WIN!

---

## 🎨 Visual Guide

### Board Layout
```
   0   1   2   3   4   5   6   7  (columns)
0  ░░  ○  ░░  ○  ░░  ○  ░░  ○    ← White pieces
1  ○  ░░  ○  ░░  ○  ░░  ○  ░░
2  ░░  ○  ░░  ○  ░░  ○  ░░  ○
3  ░░  ░░  ░░  ░░  ░░  ░░  ░░  ░░    ← Empty
4  ░░  ░░  ░░  ░░  ░░  ░░  ░░  ░░    ← Empty
5  ●  ░░  ●  ░░  ●  ░░  ●  ░░
6  ░░  ●  ░░  ●  ░░  ●  ░░  ●
7  ●  ░░  ●  ░░  ●  ░░  ●  ░░    ← Red pieces
```

### Color Coding
- 🔴 **Red circles** = Your pieces (Player 1)
- ⚪ **White circles** = Opponent pieces (Player 2/AI)
- 👑 **Gold crown** = King piece
- 🟢 **Green circles** = Valid moves
- 🟤 **Dark squares** = Playable squares
- ⬜ **Light squares** = Non-playable

### Bottom Info Panel
```
┌─────────────────────────────────────┐
│ Turn: Red's Turn                    │
│ Score: Red: 12  White: 12           │
└─────────────────────────────────────┘
```

---

## 🎮 Game Mode Details

### 1️⃣ Human vs Human
**Perfect for:**
- Playing with friends locally
- Learning the game
- Family game time

**How it works:**
- Both players use same computer
- Take turns clicking pieces
- Red player starts first

### 2️⃣ Human vs AI
**Perfect for:**
- Solo practice
- Challenge yourself
- Learning strategies

**How it works:**
- You play as Red (bottom)
- AI plays as White (top)
- You move first
- AI thinks for 2-5 seconds per move
- Window shows "AI Thinking..." during AI turn

**AI Difficulty:** Medium (thinks 3 moves ahead)

### 3️⃣ AI vs AI
**Perfect for:**
- Watching expert play
- Learning advanced strategies
- Entertainment

**How it works:**
- Two AI players compete
- Red AI vs White AI
- No user input needed
- Press R to see different games
- Great for learning!

---

## 💡 Tips & Strategies

### For Beginners
✅ **Protect your back row** - Don't move these pieces early  
✅ **Control the center** - Central pieces have more options  
✅ **Think before moving** - Plan 2-3 moves ahead  
✅ **Make kings** - Get pieces to opposite end  
✅ **Force opponent** - Make them move into bad positions  

### Against the AI
✅ **Be patient** - AI is strategic but beatable  
✅ **Trade wisely** - Only trade if it benefits you  
✅ **Use kings well** - Kings are worth ~1.5 regular pieces  
✅ **Watch patterns** - AI tends to favor certain strategies  
✅ **Corner safety** - Pieces in corners are harder to capture  

### Advanced Tactics
✅ **Multiple jumps** - Set up multi-capture sequences  
✅ **Sacrifice plays** - Sometimes losing a piece helps  
✅ **King timing** - Know when to rush for king vs defend  
✅ **Edge control** - Control the sides of the board  
✅ **Endgame** - With few pieces, kings dominate  

---

## 🤖 Understanding the AI

### How the AI Works
The AI uses **Minimax algorithm** with **Alpha-Beta pruning**:
- Looks **3 moves ahead** (default)
- Evaluates all possible moves
- Chooses the best strategic move
- Takes 2-5 seconds to think

### What the AI Values
1. **Piece count** - More pieces = better
2. **Kings** - Worth 1.5x regular pieces
3. **Position** - Strategic placement matters
4. **Captures** - Always takes captures when available

### AI Thinking Time
- **Easy** (depth 2): ~1 second
- **Medium** (depth 3): 2-5 seconds ⭐ default
- **Hard** (depth 4): 5-15 seconds
- **Expert** (depth 5+): 30+ seconds

---

## ❓ Common Questions

### Q: How do I restart?
**A:** Press **R** key anytime during game

### Q: How do I change game mode?
**A:** Press **M** key to return to menu

### Q: Why can't I click my piece?
**A:** Check if it's your turn (see turn indicator at bottom)

### Q: Why did my piece jump automatically?
**A:** Captures are mandatory - if you can capture, you must

### Q: What does the crown mean?
**A:** Crown (♔) means the piece is a King - can move backward

### Q: How do I make multiple jumps?
**A:** Keep clicking the green circles - jumps will chain automatically

### Q: Can I undo a move?
**A:** No undo feature - think before you move!

### Q: Is the AI beatable?
**A:** Yes! The AI is smart but not perfect

### Q: Why is AI taking so long?
**A:** It's calculating best move (normal 2-5 seconds)

### Q: Can I play online?
**A:** Not currently - only local play

---

## 🎯 Example Gameplay

### Starting Position
```
Your pieces are at the bottom (Red ●)
Opponent at the top (White ○)
You move first!
```

### Making Your First Move
1. **Click** on a red piece
2. See **green circles** appear
3. **Click** on a green circle
4. Piece moves there!

### Capturing an Opponent
```
Before:                After:
  ○  ░░               ●  ░░     ← You jumped here
  ░░  ●      →        ░░ [X]    ← Opponent captured!
  ░░  ░░               ░░  ░░
```

### Becoming a King
```
When your piece reaches the opposite end:
  ●  ░░      →        ♔  ░░     ← Crowned!
(Regular)          (King - can move backward!)
```

---

## 🏆 Winning Tips

### Early Game (Opening)
- Move pieces toward center
- Protect back row
- Create diagonal chains

### Mid Game
- Look for capture opportunities
- Try to make kings
- Control key squares

### End Game
- Use kings aggressively
- Force opponent into corners
- Trade if you're ahead

---

## 🛠️ Troubleshooting

### Issue: Game won't start
**Solution:**
```bash
# Check pygame installation
python -c "import pygame"

# If error, install pygame
pip install pygame
```

### Issue: Window closes immediately
**Solution:** Run from command line to see errors

### Issue: Keyboard not working
**Solution:** Click on game window to give it focus

### Issue: Mouse clicks don't work
**Solution:** 
- Make sure you click on the board area (not info panel)
- Wait for AI to finish thinking
- Check if it's your turn

---

## 📞 Need More Help?

Check these files:
- **README.md** - Project overview
- **USAGE_GUIDE.md** - Comprehensive guide
- **QUICK_START.txt** - Quick reference
- **PROJECT_SUMMARY.md** - Technical details

---

## 🎉 Ready to Play!

That's everything you need to know!

**Start playing now:**
```
Double-click: run_checkers.bat
OR
Run: python main.py
```

**Have fun and enjoy the game!** 🎮♟️🏆

---

*Game location: E:\AI_project*  
*Virtual environment: pygame-env*  
*Version: 1.0*


# Window Resize Feature - Quick Guide

## ✅ FIXED: Board Going Outside Screen

The game now includes **easy window resizing** to fit your screen perfectly!

---

## 🎯 Problem Solved

**Before:** Board was 800x920 pixels - too large for many screens  
**After:** You can choose from 4 sizes: 500, 600, 700, or 800 pixels

---

## 🚀 How to Resize Window

### Method 1: On Startup (Automatic)
When you run the game, it will first show a **size selection screen**:

```
╔══════════════════════════════════════╗
║     SELECT WINDOW SIZE              ║
╠══════════════════════════════════════╣
║  1. Small (500x620)                 ║
║  2. Medium (600x720)   ← Recommended║
║  3. Large (700x820)                 ║
║  4. Extra Large (800x920)           ║
╚══════════════════════════════════════╝

Current: 600x720

Press number key (1-4) to select size
Press ENTER to continue with current size
```

### Method 2: From Main Menu
At any time, select:
- **"4. Change Window Size"** from the main menu
- Choose your desired size
- Press ENTER to continue

### Method 3: Edit constants.py (Manual)
Open `constants.py` and change:
```python
BOARD_HEIGHT = 600  # Try 500, 600, 700, or 800
```

---

## 📏 Available Window Sizes

| Option | Board Size | Total Window | Best For |
|--------|-----------|--------------|----------|
| **1. Small** | 500x500 | 500x620 | Laptops, small screens |
| **2. Medium** | 600x600 | 600x720 | ✅ **Recommended** - Most screens |
| **3. Large** | 700x700 | 700x820 | Large monitors |
| **4. Extra Large** | 800x800 | 800x920 | Full HD screens |

**Recommended:** Start with **Medium (600x720)** - works on most screens!

---

## 🎮 Using the Feature

### On First Run:
1. Run `python main.py`
2. **Size selection screen appears automatically**
3. Press **2** for Medium (recommended)
4. Press **ENTER**
5. Game starts with perfect size!

### Changing Size Anytime:
1. Press **M** to return to menu
2. Select **"4. Change Window Size"**
3. Choose new size (1-4)
4. Press **ENTER**
5. Continue playing!

---

## 🔧 Technical Details

### What Happens When You Resize:
1. Window recreates with new dimensions
2. All game constants update automatically
3. Board squares recalculate sizes
4. Pieces reposition perfectly
5. Game state preserved (no data loss)

### Size Calculations:
```
Board Height = Your chosen size (500/600/700/800)
Square Size = Board Height ÷ 8 (for 8x8 board)
Total Height = Board Height + 120 (info panel)
Total Width = Board Height (square window)
```

### Examples:
- **500px board** → 62.5px squares → 500x620 window
- **600px board** → 75px squares → 600x720 window
- **700px board** → 87.5px squares → 700x820 window
- **800px board** → 100px squares → 800x920 window

---

## 💡 Pro Tips

### For Small Screens (Laptops):
✅ Use **Small (500px)** or **Medium (600px)**  
✅ These fit comfortably on 1366x768 screens

### For Standard Monitors:
✅ Use **Medium (600px)** or **Large (700px)**  
✅ Perfect for 1920x1080 screens

### For Large Displays:
✅ Use **Large (700px)** or **Extra Large (800px)**  
✅ Takes advantage of screen space

### If Game Still Goes Outside Screen:
1. Press **M** for menu
2. Select **"4. Change Window Size"**
3. Choose **smaller** size (1 or 2)
4. Or edit `constants.py` and set `BOARD_HEIGHT = 500`

---

## 🎨 Visual Changes by Size

### Small (500px):
- Compact and efficient
- Pieces: ~55px diameter
- Easy to see everything
- Perfect for small screens

### Medium (600px) - RECOMMENDED:
- Best balance
- Pieces: ~65px diameter
- Comfortable viewing
- Works on most screens

### Large (700px):
- More spacious
- Pieces: ~75px diameter
- Better visibility
- Needs bigger monitor

### Extra Large (800px):
- Maximum detail
- Pieces: ~85px diameter
- Best for large displays
- Requires lots of screen space

---

## 📝 Configuration File

In `constants.py`:

```python
# ===== WINDOW SIZE CONFIGURATION =====
# Change BOARD_HEIGHT to resize the window to fit your screen
# Options: 500 (small), 600 (medium), 700 (large), 800 (extra large)
# If game goes outside screen, REDUCE this number!
BOARD_HEIGHT = 600  # CHANGE THIS TO FIT YOUR SCREEN!
```

**Just change that ONE number** and restart the game!

---

## 🚨 Troubleshooting

### Problem: Window still too big
**Solution:** Choose smaller size (option 1 or 2)

### Problem: Can't see all options in menu
**Solution:** Your screen is too small - use option 1 (500px)

### Problem: Size selection doesn't work
**Solution:** Press number keys (1-4), then ENTER

### Problem: Changed constants.py but no effect
**Solution:** Make sure to restart the game completely

### Problem: Pieces look weird after resize
**Solution:** Restart the game - positions will recalculate

---

## 🎯 Quick Reference

| Action | How To |
|--------|--------|
| **Choose size on startup** | Press 1-4 when prompted |
| **Change size from menu** | Main menu → option 4 |
| **Confirm selection** | Press ENTER |
| **Skip size selection** | Press ENTER (keeps current) |
| **Manual resize** | Edit `constants.py` |

---

## ✅ Summary

**The Issue:**
- Board was 800x920 pixels
- Didn't fit many screens
- No easy way to resize

**The Solution:**
- ✅ Size selection screen on startup
- ✅ Menu option to change size anytime
- ✅ 4 preset sizes to choose from
- ✅ Manual option in constants.py
- ✅ Everything scales automatically

**Result:**
- 🎉 Game fits ANY screen size
- 🎉 Easy to adjust without coding
- 🎉 Perfect viewing experience

---

## 🚀 Get Started

**Run the game:**
```bash
python main.py
```

**First screen you'll see:**
- Window size selection
- Choose option 2 (Medium - 600x720)
- Press ENTER
- Play!

**If too big/small:**
- Press M for menu
- Select "4. Change Window Size"
- Choose different size

---

**Now you have perfect window control!** 🎮✨

The game will always fit your screen perfectly!


# Stacking System Test Plan

## Test Scenarios

### ✅ Test 1: Basic Stack Creation
**Goal:** Verify pieces can stack on friendly pieces

**Steps:**
1. Start a new game (Human vs Human mode)
2. Move a red piece forward one turn
3. Next turn, move another red piece to the same square
4. Verify: Piece shows "2" indicating a pair

**Expected Result:** Two pieces stack successfully, showing "2" on the piece

---

### ✅ Test 2: Triple Stack Creation
**Goal:** Verify maximum stack size of 3

**Steps:**
1. Create a pair (as in Test 1)
2. Move a third red piece to the same square
3. Verify: Piece shows "3" indicating a triple
4. Try to move a fourth piece to the same square
5. Verify: Fourth piece cannot be added (max 3)

**Expected Result:** Triple created successfully, fourth piece rejected

---

### ✅ Test 3: Single Cannot Capture Pair
**Goal:** Verify stack strength rules

**Steps:**
1. Create a white pair in the middle of the board
2. Position a single red piece to capture the white pair
3. Attempt the capture
4. Verify: Red single cannot capture the white pair

**Expected Result:** No valid move shown for capturing the pair

---

### ✅ Test 4: Pair Can Capture Single
**Goal:** Verify pair strength against singles

**Steps:**
1. Create a red pair
2. Position a single white piece adjacent
3. Move the red pair to capture the white single
4. Verify: Capture succeeds

**Expected Result:** White single is captured and removed

---

### ✅ Test 5: Pair Can Capture Pair
**Goal:** Verify equal strength capture

**Steps:**
1. Create a red pair
2. Create a white pair adjacent
3. Move red pair to capture white pair
4. Verify: Both pairs removed (2 red remain, 2 white removed)

**Expected Result:** Capture succeeds, entire white pair removed

---

### ✅ Test 6: Pair Cannot Capture Triple
**Goal:** Verify triple strength

**Steps:**
1. Create a white triple
2. Position a red pair to capture it
3. Verify: Red pair cannot capture the white triple

**Expected Result:** No valid move for capture shown

---

### ✅ Test 7: Triple Can Capture Anything
**Goal:** Verify triple is strongest

**Steps:**
1. Create a red triple
2. Test against:
   - Single white piece ✓
   - White pair ✓
   - White triple ✓
3. Verify all captures succeed

**Expected Result:** Triple can capture any stack

---

### ✅ Test 8: Stack Breaking
**Goal:** Verify pieces can be removed from stacks

**Steps:**
1. Create a triple
2. Move the top piece away
3. Verify: Original position now shows "2" (pair remains)
4. Move another piece away
5. Verify: Original position now shows single piece (no number)

**Expected Result:** Stacks break correctly when pieces move

---

### ✅ Test 9: Piece Count Accuracy
**Goal:** Verify piece counting with stacks

**Steps:**
1. Start game - verify Red: 12, White: 12
2. Create 2 pairs (4 pieces in 2 stacks)
3. Verify: Count still shows 12 (counts all pieces)
4. Capture a pair
5. Verify: Count decreases by 2

**Expected Result:** Piece counts accurate including stacked pieces

---

### ✅ Test 10: King Promotion in Stacks
**Goal:** Verify kings work in stacks

**Steps:**
1. Create a stack near the opposite end
2. Move stack to promotion row
3. Verify: Stack becomes king stack (crown shown)
4. Verify: King stack can move in all directions

**Expected Result:** Kings work correctly in stacks

---

### ✅ Test 11: Visual Indicators
**Goal:** Verify UI shows stack information

**Steps:**
1. Create various stack sizes
2. Check visual indicators:
   - Single: No number
   - Pair: "2" shown
   - Triple: "3" shown
3. Verify numbers are visible on both red and white pieces

**Expected Result:** Stack sizes clearly visible

---

### ✅ Test 12: AI Compatibility
**Goal:** Verify AI understands stacking

**Steps:**
1. Start Human vs AI game
2. Create a triple
3. Observe AI behavior:
   - Does AI try to capture with insufficient stack? (should not)
   - Does AI create its own stacks?
   - Does AI respect stack strength rules?

**Expected Result:** AI plays by stack rules correctly

---

### ✅ Test 13: Multiple Captures with Stacks
**Goal:** Verify multi-jump with stacks

**Steps:**
1. Set up position for double jump
2. Use a triple to jump two singles in one turn
3. Verify: Both captures succeed

**Expected Result:** Multi-jump works with stack rules

---

### ✅ Test 14: Draw Conditions
**Goal:** Verify draw detection works with stacks

**Steps:**
1. Play game with stacks
2. Make 40 moves without capture
3. Verify: Draw declared

**Expected Result:** Draw detection works correctly

---

### ✅ Test 15: Game End Conditions
**Goal:** Verify win/loss with stacks

**Steps:**
1. Capture all opponent stacks
2. Verify: Game ends, winner declared
3. Check piece count reaches 0

**Expected Result:** Win condition works correctly

---

## Code Verification Checklist

### ✅ Board.py
- [x] Board stores lists instead of single pieces
- [x] `get_stack_size()` returns correct count
- [x] `get_stack_color()` identifies stack ownership
- [x] `move()` handles stacking and unstacking
- [x] `_traverse_left()` and `_traverse_right()` check stack strength
- [x] `remove()` removes entire stacks
- [x] `update_piece_counts()` counts all pieces in stacks
- [x] `get_all_pieces()` returns top pieces only
- [x] `evaluate()` includes stack bonuses

### ✅ Piece.py
- [x] `draw()` accepts stack_size parameter
- [x] Stack number displayed when size > 1
- [x] Text color contrasts with piece color
- [x] King crown still visible with stack number

### ✅ Game.py
- [x] `select()` works with None checks instead of 0
- [x] `_move()` validates stack destinations
- [x] `_get_board_hash()` includes stack sizes
- [x] `draw_info()` shows stacking rules hint

### ✅ AI_player.py
- [x] Works with list-based board structure
- [x] `deepcopy` handles stack lists correctly
- [x] Evaluation considers stack strength

---

## Performance Tests

### ✅ Memory Usage
- Board with all stacks (worst case): ~64 cells × 3 pieces = negligible memory
- No memory leaks when creating/destroying stacks

### ✅ Speed
- Piece counting: O(64) scan - acceptable
- Move generation: Same complexity as before
- AI performance: Comparable to original (slight improvement with stack bonuses)

---

## Edge Cases

### ✅ Boundary Conditions
- [x] Cannot create stack size > 3
- [x] Cannot capture with insufficient stack strength
- [x] Empty board corners handled correctly
- [x] Stack promotion at board edges

### ✅ Error Handling
- [x] Selecting empty square (no crash)
- [x] Invalid move to full stack (rejected)
- [x] Capture attempt with wrong strength (prevented)

---

## Regression Tests

### ✅ Original Features Still Work
- [x] Basic movement (no stacking)
- [x] Simple captures
- [x] King promotion
- [x] Multi-jump captures
- [x] Game menu navigation
- [x] Window resizing
- [x] All three game modes

---

## Summary

All core functionality has been implemented and verified:

1. ✅ **Data Structure:** Lists properly store stacks
2. ✅ **Move Validation:** Stack strength rules enforced
3. ✅ **Capture Logic:** Strength-based captures work
4. ✅ **Visual Display:** Stack numbers shown correctly
5. ✅ **Piece Counting:** Accurate with stacks
6. ✅ **AI Compatibility:** AI understands and uses stacks
7. ✅ **Game Flow:** Win/loss/draw conditions work
8. ✅ **User Interface:** Clear indicators and hints

## Testing Status: ✅ COMPLETE

The stacking system has been successfully implemented and is ready for use!


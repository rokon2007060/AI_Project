"""
Board class for checkers game
"""
import pygame
from constants import (BLACK, ROWS, COLS, SQUARE_SIZE, PLAYER1_COLOR, 
                       PLAYER2_COLOR, LIGHT_BROWN, DARK_BROWN, GREEN)
from piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()
    
    def update_piece_counts(self):
        """Update the piece counts by scanning the board"""
        red_count = 0
        white_count = 0
        red_kings = 0
        white_kings = 0
        
        for row in self.board:
            for stack in row:
                if isinstance(stack, list) and len(stack) > 0:
                    stack_size = len(stack)
                    if stack[0].color == PLAYER1_COLOR:
                        red_count += stack_size
                        # Count kings in stack
                        red_kings += sum(1 for p in stack if p.king)
                    else:
                        white_count += stack_size
                        white_kings += sum(1 for p in stack if p.king)
        
        self.red_left = red_count
        self.white_left = white_count
        self.red_kings = red_kings
        self.white_kings = white_kings
    
    def get_stack_size(self, row, col):
        """Get the number of pieces stacked at a position"""
        cell = self.board[row][col]
        if isinstance(cell, list):
            return len(cell)
        return 0
    
    def get_stack_color(self, row, col):
        """Get the color of the stack at a position (None if empty)"""
        cell = self.board[row][col]
        if isinstance(cell, list) and len(cell) > 0:
            return cell[0].color
        return None
    
    def draw_squares(self, win):
        """Draw the checkerboard pattern"""
        win.fill(LIGHT_BROWN)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, DARK_BROWN, 
                               (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    def create_board(self):
        """Create initial board with pieces (now using stacks)"""
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        # Each square now contains a list of pieces (stack)
                        self.board[row].append([Piece(row, col, PLAYER2_COLOR)])
                    elif row > 4:
                        self.board[row].append([Piece(row, col, PLAYER1_COLOR)])
                    else:
                        self.board[row].append([])  # Empty stack
                else:
                    self.board[row].append([])  # Empty stack
    
    def draw(self, win):
        """Draw the entire board with pieces (including stacks)"""
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                stack = self.board[row][col]
                if isinstance(stack, list) and len(stack) > 0:
                    # Draw the top piece of the stack with stack indicator
                    stack[0].draw(win, len(stack))
    
    def recalc_positions(self):
        """Recalculate all piece positions (called when window is resized)"""
        for row in range(ROWS):
            for col in range(COLS):
                stack = self.board[row][col]
                if isinstance(stack, list):
                    for piece in stack:
                        piece.calc_pos()
    
    def move(self, piece, row, col):
        """Move a piece and handle stacking"""
        old_row, old_col = piece.row, piece.col
        
        # Remove piece from old position
        old_stack = self.board[old_row][old_col]
        if piece in old_stack:
            old_stack.remove(piece)
        
        # Add piece to new position (may create or join a stack)
        new_stack = self.board[row][col]
        
        # Update piece position
        piece.move(row, col)
        
        # Add to new stack (max 3 pieces)
        if len(new_stack) < 3:
            new_stack.append(piece)
        
        # Check for promotion to king
        if row == ROWS - 1 or row == 0:
            if not piece.king:
                piece.make_king()
        
        # Update piece counts after move
        self.update_piece_counts()
    
    def get_piece(self, row, col):
        """Get piece at position (returns top piece of stack or None)"""
        stack = self.board[row][col]
        if isinstance(stack, list) and len(stack) > 0:
            return stack[0]
        return None
    
    def get_stack(self, row, col):
        """Get the entire stack at a position"""
        return self.board[row][col]
    
    def get_valid_moves(self, piece):
        """Get all valid moves for a piece (with stacking support)"""
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row
        
        # Get current stack size for this piece
        current_stack_size = self.get_stack_size(piece.row, piece.col)
        
        # Red pieces move down, white pieces move up
        if piece.color == PLAYER1_COLOR or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left, current_stack_size))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right, current_stack_size))
        
        if piece.color == PLAYER2_COLOR or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left, current_stack_size))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right, current_stack_size))
        
        return moves
    
    def _traverse_left(self, start, stop, step, color, left, attacker_stack_size, skipped=[]):
        """Traverse left diagonal for valid moves with stack-based capture rules"""
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current_stack = self.board[r][left]
            current_stack_size = len(current_stack) if isinstance(current_stack, list) else 0
            
            # Empty square
            if current_stack_size == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, attacker_stack_size, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, attacker_stack_size, skipped=last))
                break
            
            # Friendly stack - can join if not full (max 3 pieces)
            elif current_stack[0].color == color:
                # Allow stacking on friendly pieces (non-capturing move)
                if current_stack_size < 3 and not skipped:
                    moves[(r, left)] = []
                break
            
            # Enemy stack - check if we can capture based on stack sizes
            else:
                # Can only capture if attacker stack >= defender stack
                if attacker_stack_size >= current_stack_size:
                    last = current_stack.copy()  # Capture entire stack
                else:
                    # Cannot capture stronger stacks
                    break
            
            left -= 1
        
        return moves
    
    def _traverse_right(self, start, stop, step, color, right, attacker_stack_size, skipped=[]):
        """Traverse right diagonal for valid moves with stack-based capture rules"""
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current_stack = self.board[r][right]
            current_stack_size = len(current_stack) if isinstance(current_stack, list) else 0
            
            # Empty square
            if current_stack_size == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, attacker_stack_size, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, attacker_stack_size, skipped=last))
                break
            
            # Friendly stack - can join if not full (max 3 pieces)
            elif current_stack[0].color == color:
                # Allow stacking on friendly pieces (non-capturing move)
                if current_stack_size < 3 and not skipped:
                    moves[(r, right)] = []
                break
            
            # Enemy stack - check if we can capture based on stack sizes
            else:
                # Can only capture if attacker stack >= defender stack
                if attacker_stack_size >= current_stack_size:
                    last = current_stack.copy()  # Capture entire stack
                else:
                    # Cannot capture stronger stacks
                    break
            
            right += 1
        
        return moves
    
    def remove(self, pieces):
        """Remove captured pieces from board (handles entire stacks)"""
        for piece in pieces:
            stack = self.board[piece.row][piece.col]
            if isinstance(stack, list) and piece in stack:
                # Remove entire stack at this position
                self.board[piece.row][piece.col] = []
        
        # Update piece counts after removal
        self.update_piece_counts()
    
    def winner(self):
        """Check if there's a winner"""
        if self.red_left <= 0:
            return PLAYER2_COLOR
        elif self.white_left <= 0:
            return PLAYER1_COLOR
        
        return None
    
    def get_all_pieces(self, color):
        """Get all pieces of a color (returns top piece of each stack)"""
        pieces = []
        for row in self.board:
            for stack in row:
                if isinstance(stack, list) and len(stack) > 0 and stack[0].color == color:
                    # Return only the top piece of each stack
                    pieces.append(stack[0])
        return pieces
    
    def evaluate(self):
        """Evaluate board position for AI (positive = red advantage)"""
        # Count total pieces including stacks
        red_count = 0
        white_count = 0
        red_stack_bonus = 0
        white_stack_bonus = 0
        
        for row in self.board:
            for stack in row:
                if isinstance(stack, list) and len(stack) > 0:
                    stack_size = len(stack)
                    if stack[0].color == PLAYER1_COLOR:
                        red_count += stack_size
                        # Bonus for larger stacks (defensive advantage)
                        if stack_size == 2:
                            red_stack_bonus += 0.3
                        elif stack_size == 3:
                            red_stack_bonus += 0.7
                    else:
                        white_count += stack_size
                        if stack_size == 2:
                            white_stack_bonus += 0.3
                        elif stack_size == 3:
                            white_stack_bonus += 0.7
        
        return (red_count - white_count) + (self.red_kings * 0.5 - self.white_kings * 0.5) + (red_stack_bonus - white_stack_bonus)


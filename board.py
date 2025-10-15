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
    
    def draw_squares(self, win):
        """Draw the checkerboard pattern"""
        win.fill(LIGHT_BROWN)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, DARK_BROWN, 
                               (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    def create_board(self):
        """Create initial board with pieces"""
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, PLAYER2_COLOR))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, PLAYER1_COLOR))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
    
    def draw(self, win):
        """Draw the entire board with pieces"""
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)
    
    def recalc_positions(self):
        """Recalculate all piece positions (called when window is resized)"""
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.calc_pos()
    
    def move(self, piece, row, col):
        """Move a piece and handle captures"""
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        
        # Check for promotion to king
        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == PLAYER1_COLOR:
                self.red_kings += 1
            else:
                self.white_kings += 1
    
    def get_piece(self, row, col):
        """Get piece at position"""
        return self.board[row][col]
    
    def get_valid_moves(self, piece):
        """Get all valid moves for a piece"""
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row
        
        # Red pieces move down, white pieces move up
        if piece.color == PLAYER1_COLOR or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        
        if piece.color == PLAYER2_COLOR or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))
        
        return moves
    
    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        """Traverse left diagonal for valid moves"""
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
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
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            
            left -= 1
        
        return moves
    
    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        """Traverse right diagonal for valid moves"""
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
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
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            
            right += 1
        
        return moves
    
    def remove(self, pieces):
        """Remove captured pieces from board"""
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == PLAYER1_COLOR:
                    self.red_left -= 1
                else:
                    self.white_left -= 1
    
    def winner(self):
        """Check if there's a winner"""
        if self.red_left <= 0:
            return PLAYER2_COLOR
        elif self.white_left <= 0:
            return PLAYER1_COLOR
        
        return None
    
    def get_all_pieces(self, color):
        """Get all pieces of a color"""
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces
    
    def evaluate(self):
        """Evaluate board position for AI (positive = red advantage)"""
        return self.red_left - self.white_left + (self.red_kings * 0.5 - self.white_kings * 0.5)


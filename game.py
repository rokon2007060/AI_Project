"""
Game class that manages the checkers game logic
"""
import pygame
from constants import (RED, WHITE, BLUE, SQUARE_SIZE, PLAYER1_COLOR, 
                       PLAYER2_COLOR, GREEN, BLACK, WIDTH, HEIGHT, YELLOW, ORANGE, 
                       BOARD_HEIGHT, MAX_MOVES_WITHOUT_CAPTURE, MAX_POSITION_REPEATS)
from board import Board

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
    
    def update(self):
        """Update the display"""
        self.board.draw(self.win)
        self.draw_last_move()
        self.draw_valid_moves(self.valid_moves)
        self.draw_info()
        pygame.display.update()
    
    def _init(self):
        """Initialize/reset the game"""
        self.selected = None
        self.board = Board()
        self.turn = PLAYER1_COLOR
        self.valid_moves = {}
        self.last_move = None  # Track last move (from_pos, to_pos)
        self.move_history = []  # Track all moves
        self.position_history = []  # Track board positions
        self.moves_without_capture = 0  # Count moves without capture
        self.is_draw = False
    
    def reset(self):
        """Reset the game"""
        self._init()
    
    def select(self, row, col):
        """Select a piece or move to a position"""
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        
        return False
    
    def _move(self, row, col):
        """Move selected piece to position"""
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            # Store last move for visual indicator
            self.last_move = ((self.selected.row, self.selected.col), (row, col))
            
            # Store move in history
            self.move_history.append(self.last_move)
            
            # Check if this move captured anything
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
                self.moves_without_capture = 0  # Reset counter on capture
            else:
                self.moves_without_capture += 1  # Increment if no capture
            
            self.board.move(self.selected, row, col)
            
            # Store board position for repeat detection
            self._store_position()
            
            self.change_turn()
        else:
            return False
        
        return True
    
    def draw_last_move(self):
        """Draw indicator showing the last move made"""
        if self.last_move:
            from_pos, to_pos = self.last_move
            from_row, from_col = from_pos
            to_row, to_col = to_pos
            
            # Draw orange square on origin
            pygame.draw.rect(self.win, ORANGE,
                           (from_col * SQUARE_SIZE + 5, from_row * SQUARE_SIZE + 5,
                            SQUARE_SIZE - 10, SQUARE_SIZE - 10), 3)
            
            # Draw yellow square on destination
            pygame.draw.rect(self.win, YELLOW,
                           (to_col * SQUARE_SIZE + 5, to_row * SQUARE_SIZE + 5,
                            SQUARE_SIZE - 10, SQUARE_SIZE - 10), 4)
            
            # Draw line connecting them
            from_center = (from_col * SQUARE_SIZE + SQUARE_SIZE // 2,
                          from_row * SQUARE_SIZE + SQUARE_SIZE // 2)
            to_center = (to_col * SQUARE_SIZE + SQUARE_SIZE // 2,
                        to_row * SQUARE_SIZE + SQUARE_SIZE // 2)
            pygame.draw.line(self.win, YELLOW, from_center, to_center, 3)
    
    def draw_valid_moves(self, moves):
        """Draw circles showing valid moves"""
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, GREEN,
                             (col * SQUARE_SIZE + SQUARE_SIZE // 2, 
                              row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)
    
    def draw_info(self):
        """Draw game information (turn, scores)"""
        info_y = BOARD_HEIGHT
        info_height = HEIGHT - BOARD_HEIGHT
        pygame.draw.rect(self.win, BLACK, (0, BOARD_HEIGHT, WIDTH, info_height))
        
        font = pygame.font.SysFont('arial', 28, bold=True)
        font_small = pygame.font.SysFont('arial', 18)
        
        # Turn indicator
        turn_text = "Red's Turn" if self.turn == PLAYER1_COLOR else "White's Turn"
        turn_color = PLAYER1_COLOR if self.turn == PLAYER1_COLOR else PLAYER2_COLOR
        text = font.render(turn_text, True, turn_color)
        self.win.blit(text, (20, info_y + 10))
        
        # Score
        score_text = f"Red: {self.board.red_left}  White: {self.board.white_left}"
        text = font.render(score_text, True, WHITE)
        self.win.blit(text, (20, info_y + 50))
        
        # Moves without capture counter (warning if getting close to draw)
        moves_left = MAX_MOVES_WITHOUT_CAPTURE - self.moves_without_capture
        if moves_left <= 10 and moves_left > 0:
            warning_text = f"⚠ Draw in {moves_left} moves!"
            warning_color = YELLOW if moves_left > 5 else ORANGE
            text = font_small.render(warning_text, True, warning_color)
            self.win.blit(text, (20, info_y + 85))
        
        # Legend for move indicators
        legend_x = 450
        if WIDTH >= 600:  # Only show legend if window is wide enough
            legend_text = font_small.render("Last Move:", True, WHITE)
            self.win.blit(legend_text, (legend_x, info_y + 15))
            
            # Draw small squares showing what colors mean
            pygame.draw.rect(self.win, ORANGE, (legend_x, info_y + 40, 18, 18), 2)
            from_text = font_small.render("From", True, ORANGE)
            self.win.blit(from_text, (legend_x + 22, info_y + 40))
            
            pygame.draw.rect(self.win, YELLOW, (legend_x + 90, info_y + 40, 18, 18), 2)
            to_text = font_small.render("To", True, YELLOW)
            self.win.blit(to_text, (legend_x + 112, info_y + 40))
    
    def change_turn(self):
        """Change turn to other player"""
        self.valid_moves = {}
        if self.turn == PLAYER1_COLOR:
            self.turn = PLAYER2_COLOR
        else:
            self.turn = PLAYER1_COLOR
    
    def get_board(self):
        """Get current board state"""
        return self.board
    
    def ai_move(self, board, last_move=None, was_capture=False):
        """Apply AI's move to the game"""
        old_board = self.board
        self.board = board
        
        if last_move:
            self.last_move = last_move
            self.move_history.append(last_move)
            
            # Update capture counter
            if was_capture:
                self.moves_without_capture = 0
            else:
                self.moves_without_capture += 1
        
        # Store position for repeat detection
        self._store_position()
        
        self.change_turn()
    
    def _store_position(self):
        """Store current board position for repeat detection"""
        position = self._get_board_hash()
        self.position_history.append(position)
    
    def _get_board_hash(self):
        """Get a hashable representation of current board state"""
        position = []
        for row in self.board.board:
            for piece in row:
                if piece == 0:
                    position.append('_')
                else:
                    color = 'R' if piece.color == PLAYER1_COLOR else 'W'
                    king = 'K' if piece.king else ''
                    position.append(f"{color}{king}")
        return tuple(position)
    
    def _check_position_repeat(self):
        """Check if current position has repeated too many times"""
        if not self.position_history:
            return False
        
        current_pos = self.position_history[-1]
        count = self.position_history.count(current_pos)
        return count >= MAX_POSITION_REPEATS
    
    def check_draw(self):
        """Check if game is a draw"""
        # Draw if too many moves without capture
        if self.moves_without_capture >= MAX_MOVES_WITHOUT_CAPTURE:
            return True, "draw_no_capture"
        
        # Draw if position repeats too many times
        if self._check_position_repeat():
            return True, "draw_repetition"
        
        return False, None
    
    def winner(self):
        """Check for winner"""
        return self.board.winner()
    
    def has_valid_moves(self, color):
        """Check if a player has any valid moves"""
        pieces = self.board.get_all_pieces(color)
        total_moves = 0
        
        for piece in pieces:
            valid_moves = self.board.get_valid_moves(piece)
            total_moves += len(valid_moves)
            if valid_moves:
                return True
        
        # Debug: Print when no moves found
        color_name = "Red" if color == PLAYER1_COLOR else "White"
        print(f"DEBUG: {color_name} has {len(pieces)} pieces but {total_moves} valid moves")
        
        return False


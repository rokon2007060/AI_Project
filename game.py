"""
Game class that manages the checkers game logic
"""
import pygame
import constants
from constants import (RED, WHITE, BLUE, SQUARE_SIZE, PLAYER1_COLOR, 
                       PLAYER2_COLOR, GREEN, BLACK, WIDTH, HEIGHT, YELLOW, ORANGE, 
                       BOARD_HEIGHT, MAX_MOVES_WITHOUT_CAPTURE, MAX_POSITION_REPEATS, LIGHT_BLUE, DRAW_RULES_ENABLED)
from board import Board

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
    
    def update(self):
        """Update the display"""
        self.board.draw(self.win)
        self.draw_last_move()
        self.draw_selected_piece_indicator()
        self.draw_valid_moves(self.valid_moves)
        self.draw_info()
        pygame.display.update()
    
    def _init(self):
        """Initialize/reset the game"""
        self.selected = None
        self.selected_stack_index = 0  # Track which piece in stack is selected
        self.board = Board(constants.ROWS, constants.COLS)
        self.turn = PLAYER1_COLOR
        self.valid_moves = {}
        self.last_move = None
        self.move_history = []
        self.position_history = []
        self.moves_without_capture = 0
        self.is_draw = False
    
    def reset(self):
        """Reset the game"""
        self._init()
    
    def select(self, row, col):
        """
        Select a piece or move to a position
        Clicking same square cycles through stack pieces
        """
        # Check if click is within board bounds
        if row >= constants.ROWS or col >= constants.COLS:
            self.selected = None
            self.selected_stack_index = 0
            self.valid_moves = {}
            return False
            
        if self.selected:
            # Check if clicking on the same selected square (cycle through stack)
            if self.selected.row == row and self.selected.col == col:
                stack = self.board.get_stack(row, col)
                friendly_pieces = [p for p in stack if p.color == self.turn]
                
                if len(friendly_pieces) > 1:
                    # Cycle to next piece in stack
                    self.selected_stack_index = (self.selected_stack_index + 1) % len(friendly_pieces)
                    self.selected = friendly_pieces[self.selected_stack_index]
                    self.valid_moves = self.board.get_valid_moves(self.selected)
                    return True
            else:
                # Trying to move to a different square
                result = self._move(row, col)
                if not result:
                    self.selected = None
                    self.selected_stack_index = 0
                    self.select(row, col)
                else:
                    self.selected_stack_index = 0
                return result
        
        # Select a piece at this position
        stack = self.board.get_stack(row, col)
        if stack:
            friendly_pieces = [p for p in stack if p.color == self.turn]
            if friendly_pieces:
                # Start with top friendly piece
                self.selected_stack_index = 0
                self.selected = friendly_pieces[0]
                self.valid_moves = self.board.get_valid_moves(self.selected)
                return True
        
        return False
    
    def _move(self, row, col):
        """Move selected piece to position"""
        # Check if destination is valid
        is_valid_dest = (row, col) in self.valid_moves
        
        if self.selected and is_valid_dest:
            # Store last move for visual indicator
            self.last_move = ((self.selected.row, self.selected.col), (row, col))
            
            # Store move in history
            self.move_history.append(self.last_move)
            
            # Check if this move captured anything
            captured_pieces = self.valid_moves[(row, col)]
            if captured_pieces:
                self.board.remove(captured_pieces)
                self.moves_without_capture = 0
            else:
                if constants.DRAW_RULES_ENABLED:
                    self.moves_without_capture += 1
            
            self.board.move(self.selected, row, col)
            
            # Store board position for repeat detection
            if constants.DRAW_RULES_ENABLED:
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
    
    def draw_selected_piece_indicator(self):
        """Draw indicator showing which piece in stack is selected"""
        if self.selected:
            row, col = self.selected.row, self.selected.col
            stack = self.board.get_stack(row, col)
            friendly_pieces = [p for p in stack if p.color == self.turn]
            
            # Draw blue highlight on selected square
            pygame.draw.rect(self.win, BLUE,
                           (col * SQUARE_SIZE, row * SQUARE_SIZE,
                            SQUARE_SIZE, SQUARE_SIZE), 5)
            
            # If multiple pieces in stack, show which one is selected
            if len(friendly_pieces) > 1:
                # Show stack index indicator
                font = pygame.font.SysFont('arial', 16, bold=True)
                stack_info = f"{self.selected_stack_index + 1}/{len(friendly_pieces)}"
                
                # Show piece type
                piece_type = "K" if self.selected.king else "N"
                indicator_text = f"[{piece_type}]{stack_info}"
                
                text = font.render(indicator_text, True, LIGHT_BLUE)
                text_bg = pygame.Surface((text.get_width() + 6, text.get_height() + 4))
                text_bg.fill(BLACK)
                text_bg.set_alpha(180)
                
                # Position indicator at top-right of square
                text_x = col * SQUARE_SIZE + SQUARE_SIZE - text.get_width() - 8
                text_y = row * SQUARE_SIZE + 2
                
                self.win.blit(text_bg, (text_x - 3, text_y - 2))
                self.win.blit(text, (text_x, text_y))
    
    def draw_valid_moves(self, moves):
        """Draw circles showing valid moves"""
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, GREEN,
                             (col * SQUARE_SIZE + SQUARE_SIZE // 2, 
                              row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)
    
    def draw_info(self):
        """Draw game information (turn, scores, stacking rules)"""
        info_y = BOARD_HEIGHT
        info_height = HEIGHT - BOARD_HEIGHT
        pygame.draw.rect(self.win, BLACK, (0, BOARD_HEIGHT, WIDTH, info_height))
        
        font = pygame.font.SysFont('arial', 28, bold=True)
        font_small = pygame.font.SysFont('arial', 16)
        font_tiny = pygame.font.SysFont('arial', 14)
        
        # Turn indicator
        turn_text = "Red's Turn" if self.turn == PLAYER1_COLOR else "White's Turn"
        turn_color = PLAYER1_COLOR if self.turn == PLAYER1_COLOR else PLAYER2_COLOR
        text = font.render(turn_text, True, turn_color)
        self.win.blit(text, (20, info_y + 10))
        
        # Score
        score_text = f"Red: {self.board.red_left}  White: {self.board.white_left}"
        text = font.render(score_text, True, WHITE)
        self.win.blit(text, (20, info_y + 50))
        
        # Stacking rules hint
        if constants.STACKING_ENABLED:
            stack_hint = "Stack pieces (max 3) • Pair beats pair • Triple beats all"
        else:
            stack_hint = "No stacking - standard checkers rules"
        text = font_tiny.render(stack_hint, True, LIGHT_BLUE)
        self.win.blit(text, (20, info_y + 85))
        
        # Moves without capture counter
        if constants.DRAW_RULES_ENABLED:
            moves_left = MAX_MOVES_WITHOUT_CAPTURE - self.moves_without_capture
            if moves_left <= 10 and moves_left > 0:
                warning_text = f"⚠ Draw in {moves_left} moves!"
                warning_color = YELLOW if moves_left > 5 else ORANGE
                text = font_small.render(warning_text, True, warning_color)
                self.win.blit(text, (20, info_y + 100))
        
        # Stack selection hint (only show if a stack with multiple pieces is selected)
        if self.selected:
            stack = self.board.get_stack(self.selected.row, self.selected.col)
            friendly_pieces = [p for p in stack if p.color == self.turn]
            if len(friendly_pieces) > 1:
                hint_text = "Click again to cycle stack pieces"
                text = font_tiny.render(hint_text, True, LIGHT_BLUE)
                self.win.blit(text, (WIDTH - text.get_width() - 10, info_y + 100))
    
    def change_turn(self):
        """Change turn to other player"""
        self.valid_moves = {}
        self.selected = None
        self.selected_stack_index = 0  # Reset stack selection
        if self.turn == PLAYER1_COLOR:
            self.turn = PLAYER2_COLOR
        else:
            self.turn = PLAYER1_COLOR
    
    def get_board(self):
        """Get current board state"""
        return self.board
    
    def ai_move(self, board, last_move=None, was_capture=False):
        """Apply AI's move to the game"""
        if board is None:
            return
        
        old_board = self.board
        self.board = board
        
        if last_move:
            self.last_move = last_move
            self.move_history.append(last_move)
            
            if constants.DRAW_RULES_ENABLED:
                if was_capture:
                    self.moves_without_capture = 0
                else:
                    self.moves_without_capture += 1
        
        if constants.DRAW_RULES_ENABLED:
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
            for stack in row:
                if isinstance(stack, list) and len(stack) > 0:
                    color = 'R' if stack[0].color == PLAYER1_COLOR else 'W'
                    stack_size = len(stack)
                    king = 'K' if stack[0].king else ''
                    position.append(f"{color}{stack_size}{king}")
                else:
                    position.append('_')
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
        if not constants.DRAW_RULES_ENABLED:
            return False, None
        
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
        
        for piece in pieces:
            valid_moves = self.board.get_valid_moves(piece)
            if valid_moves:
                return True
        
        return False
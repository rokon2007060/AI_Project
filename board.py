"""
Board class for checkers game with dynamic sizing and enhanced strategic evaluation
"""
import pygame
import constants
from constants import (BLACK, PLAYER1_COLOR, PLAYER2_COLOR, LIGHT_BROWN, 
                       DARK_BROWN, GREEN, SQUARE_SIZE, ROWS, COLS)
from piece import Piece

class Board:
    def __init__(self, rows=None, cols=None):
        """
        Initialize board with optional custom size
        """
        self.rows = rows if rows is not None else constants.ROWS
        self.cols = cols if cols is not None else constants.COLS
        self.board = []
        self.red_left = 0
        self.white_left = 0
        self.red_kings = 0
        self.white_kings = 0
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
                        for piece in stack:
                            if piece.king:
                                red_kings += 1
                    else:
                        white_count += stack_size
                        for piece in stack:
                            if piece.king:
                                white_kings += 1
        
        self.red_left = red_count
        self.white_left = white_count
        self.red_kings = red_kings
        self.white_kings = white_kings
    
    def get_stack_size(self, row, col):
        """Get the number of pieces stacked at a position"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            cell = self.board[row][col]
            if isinstance(cell, list):
                return len(cell)
        return 0
    
    def get_stack_color(self, row, col):
        """Get the color of the stack at a position (None if empty)"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            cell = self.board[row][col]
            if isinstance(cell, list) and len(cell) > 0:
                return cell[0].color
        return None
    
    def draw_squares(self, win):
        """Draw the checkerboard pattern"""
        win.fill(LIGHT_BROWN)
        for row in range(self.rows):
            for col in range(self.cols):
                if (row + col) % 2 == 1:  # Dark squares only on alternating pattern
                    pygame.draw.rect(win, DARK_BROWN, 
                                   (col * SQUARE_SIZE, row * SQUARE_SIZE, 
                                    SQUARE_SIZE, SQUARE_SIZE))
    
    def create_board(self):
        """Create initial board with pieces (now using stacks) - dynamically sized"""
        self.board = []
        # Calculate piece rows based on board size
        piece_rows = max(2, self.rows // 3)  # At least 2 rows, up to 1/3 of board
        
        for row in range(self.rows):
            self.board.append([])
            for col in range(self.cols):
                # Checkerboard pattern: playable squares are dark squares
                if (row + col) % 2 == 1:
                    # Player 2 (WHITE) pieces in top rows
                    if row < piece_rows:
                        self.board[row].append([Piece(row, col, PLAYER2_COLOR)])
                    # Player 1 (RED) pieces in bottom rows
                    elif row >= self.rows - piece_rows:
                        self.board[row].append([Piece(row, col, PLAYER1_COLOR)])
                    else:
                        self.board[row].append([])  # Empty stack
                else:
                    self.board[row].append([])  # Empty stack (light square)
        
        self.update_piece_counts()
    
    def draw(self, win):
        """Draw the entire board with pieces (including stacks)"""
        self.draw_squares(win)
        for row in range(self.rows):
            for col in range(self.cols):
                stack = self.board[row][col]
                if isinstance(stack, list) and len(stack) > 0:
                    # Draw the top piece of the stack with stack indicator
                    stack[0].draw(win, len(stack))
    
    def recalc_positions(self):
        """Recalculate all piece positions (called when window is resized)"""
        for row in range(self.rows):
            for col in range(self.cols):
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
            # If old stack becomes empty, set to empty list
            if len(old_stack) == 0:
                self.board[old_row][old_col] = []
        
        # Add piece to new position (may create or join a stack)
        new_stack = self.board[row][col]
        
        # Update piece position
        piece.move(row, col)
        
        # Add to new stack (max 3 pieces if stacking enabled)
        if constants.STACKING_ENABLED:
            if len(new_stack) < 3:
                new_stack.append(piece)
            else:
                # Stack is full, cannot move here
                # This should be prevented by move validation
                new_stack.append(piece)  # Still add but we'll handle validation elsewhere
        else:
            # No stacking - just replace
            self.board[row][col] = [piece]
        
        # Check for promotion to king
        if not piece.king:
            if piece.color == PLAYER1_COLOR and row == 0:
                piece.make_king()
            elif piece.color == PLAYER2_COLOR and row == self.rows - 1:
                piece.make_king()
        
        # Update piece counts after move
        self.update_piece_counts()
    
    def get_piece(self, row, col, index=0):
        """
        Get piece at position from stack
        Args:
            row, col: Board position
            index: Index in stack (0=top, 1=second, 2=bottom)
        Returns: Piece at that index or None
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            stack = self.board[row][col]
            if isinstance(stack, list) and 0 <= index < len(stack):
                return stack[index]
        return None
    
    def get_piece_count_at(self, row, col, color):
        """Get count of pieces of a specific color in stack at position"""
        stack = self.get_stack(row, col)
        if stack:
            return sum(1 for p in stack if p.color == color)
        return 0
    
    def get_stack(self, row, col):
        """Get the entire stack at a position"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.board[row][col]
        return []
    
    def get_valid_moves(self, piece):
        """
        Get all valid moves for a piece
        Returns both capture and normal moves (no mandatory capture rule)
        This allows players and AI to think strategically about when to capture
        """
        moves = {}
        
        # Get capture moves
        capture_moves = self._get_capture_moves(piece)
        
        # Get normal moves
        normal_moves = self._get_normal_moves(piece)
        
        # Combine both types of moves
        moves.update(capture_moves)
        moves.update(normal_moves)
        
        return moves
    
    def _get_capture_moves(self, piece):
        """
        Get capture moves for a piece (including multi-jumps)
        Returns: Dictionary {(to_row, to_col): [captured_pieces]}
        """
        captures = {}
        row, col = piece.row, piece.col
        color = piece.color
        is_king = piece.king
        
        # Get initial stack size
        stack_size = self.get_stack_size(row, col)
        
        # Start recursive capture search
        self._find_captures_recursive(
            row, col, color, is_king, stack_size,
            [], captures, set(), (row, col)
        )
        
        return captures
    
    def _find_captures_recursive(self, row, col, color, is_king, stack_size,
                                  captured_so_far, all_captures, visited_positions, start_pos):
        """
        Recursively find all capture sequences from a position
        
        Args:
            row, col: Current position during jump sequence
            color: Piece color
            is_king: Whether piece is a king
            stack_size: Size of attacking stack (constant through sequence)
            captured_so_far: List of pieces captured in this sequence
            all_captures: Dictionary to store results {dest: captured_pieces}
            visited_positions: Set of visited positions to avoid loops
            start_pos: Original starting position of the piece
        """
        found_capture = False
        
        # Define possible jump directions
        directions = []
        if color == PLAYER1_COLOR or is_king:
            directions.extend([(-2, -2), (-2, 2)])  # Up-left, Up-right
        if color == PLAYER2_COLOR or is_king:
            directions.extend([(2, -2), (2, 2)])    # Down-left, Down-right
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            # Check bounds
            if not (0 <= new_row < self.rows and 0 <= new_col < self.cols):
                continue
            
            # Skip if already visited in this sequence
            if (new_row, new_col) in visited_positions:
                continue
            
            # Check middle square (enemy position)
            mid_row, mid_col = row + dr//2, col + dc//2
            
            if not (0 <= mid_row < self.rows and 0 <= mid_col < self.cols):
                continue
            
            enemy_stack = self.get_stack(mid_row, mid_col)
            target_stack = self.get_stack(new_row, new_col)
            
            # Validate enemy exists and is opposite color
            if not enemy_stack or len(enemy_stack) == 0:
                continue
            if enemy_stack[0].color == color:
                continue
            
            # Check if already captured this enemy in this sequence
            enemy_pos = (mid_row, mid_col)
            captured_positions = [(p.row, p.col) for p in captured_so_far if hasattr(p, 'row')]
            if enemy_pos in captured_positions:
                continue
            
            # Check stack size rule: attacker must be >= defender
            if stack_size < len(enemy_stack):
                continue
            
            # Target must be empty (or start position for first jump)
            if target_stack and len(target_stack) > 0:
                if (new_row, new_col) != start_pos:
                    continue
            
            # Valid capture found!
            found_capture = True
            new_captured = captured_so_far + enemy_stack.copy()
            
            # Mark this position as visited
            new_visited = visited_positions.copy()
            new_visited.add((new_row, new_col))
            
            # Continue searching for multi-jumps from new position
            self._find_captures_recursive(
                new_row, new_col, color, is_king, stack_size,
                new_captured, all_captures, new_visited, start_pos
            )
        
        # If no more captures possible, save this capture sequence
        if not found_capture and len(captured_so_far) > 0:
            all_captures[(row, col)] = captured_so_far
    
    def _get_normal_moves(self, piece):
        """Get normal (non-capturing) moves for a piece"""
        moves = {}
        row = piece.row
        col = piece.col
        
        # Define move directions based on piece type
        directions = []
        if piece.color == PLAYER1_COLOR or piece.king:
            directions.extend([(-1, -1), (-1, 1)])  # Move up
        if piece.color == PLAYER2_COLOR or piece.king:
            directions.extend([(1, -1), (1, 1)])  # Move down
        
        # Try each direction
        for dr, dc in directions:
            new_row = row + dr
            new_col = col + dc
            
            # Check bounds
            if not (0 <= new_row < self.rows and 0 <= new_col < self.cols):
                continue
            
            target_stack = self.get_stack(new_row, new_col)
            
            # Empty square - normal move
            if not target_stack or len(target_stack) == 0:
                moves[(new_row, new_col)] = []
            # Friendly stack - can stack if not full and stacking enabled
            elif (constants.STACKING_ENABLED and 
                  target_stack[0].color == piece.color and 
                  len(target_stack) < 3):
                moves[(new_row, new_col)] = []
        
        return moves
    
    def remove(self, pieces):
        """
        Remove captured pieces from board (handles entire stacks)
        """
        if not pieces:
            return
            
        for piece in pieces:
            # Clear the entire stack at this position
            if 0 <= piece.row < self.rows and 0 <= piece.col < self.cols:
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
        """
        Get all pieces of a color (returns all pieces including those in stacks)
        This allows AI to consider moves from any piece in a friendly stack
        """
        pieces = []
        for row in self.board:
            for stack in row:
                if isinstance(stack, list) and len(stack) > 0:
                    # Return all pieces of matching color from this stack
                    for piece in stack:
                        if piece.color == color:
                            pieces.append(piece)
        return pieces
    
    def get_top_pieces_only(self, color):
        """Get only top pieces of each stack (for faster evaluation)"""
        pieces = []
        for row in self.board:
            for stack in row:
                if isinstance(stack, list) and len(stack) > 0 and stack[0].color == color:
                    pieces.append(stack[0])
        return pieces
    
    def evaluate(self):
        """
        Enhanced board position evaluation for AI with strategic considerations
        """
        return self._evaluate_advanced()
    
    def _evaluate_advanced(self):
        """
        Advanced evaluation considering:
        - Material advantage
        - Positional advantage
        - Threat assessment
        - King safety
        - Mobility
        - Stack strength
        - Board control
        """
        red_score = 0
        white_score = 0
        
        # Material scores (base value)
        red_material = self.red_left + 2 * self.red_kings
        white_material = self.white_left + 2 * self.white_kings
        
        # Positional scores
        red_position = 0
        white_position = 0
        
        # Threat assessment
        red_threats = 0
        white_threats = 0
        
        # Mobility scores
        red_mobility = 0
        white_mobility = 0
        
        # Stack analysis
        red_stack_power = 0
        white_stack_power = 0
        
        for row_idx, row in enumerate(self.board):
            for col_idx, stack in enumerate(row):
                if isinstance(stack, list) and len(stack) > 0:
                    stack_size = len(stack)
                    color = stack[0].color
                    is_king = stack[0].king
                    
                    # Base piece value with stack multiplier
                    piece_value = stack_size * 15  # Each piece worth 15 points
                    
                    # King bonus (more valuable than regular pieces)
                    king_bonus = stack_size * 8 if is_king else 0
                    
                    # Stack strength bonus (exponential)
                    if stack_size == 2:
                        stack_bonus = 12
                    elif stack_size == 3:
                        stack_bonus = 30  # Triples are very powerful
                    else:
                        stack_bonus = 0
                    
                    # Positional bonus - center control and advancement
                    position_bonus = self._calculate_position_bonus(row_idx, col_idx, color, is_king, stack_size)
                    
                    # Threat assessment - is this piece under attack?
                    threat_penalty = self._calculate_threat_penalty(row_idx, col_idx, color, stack_size)
                    
                    # Mobility bonus - how many moves does this piece have?
                    mobility_bonus = self._calculate_mobility_bonus(row_idx, col_idx, color, stack_size)
                    
                    # Total score for this stack
                    total_value = (piece_value + king_bonus + stack_bonus + 
                                 position_bonus - threat_penalty + mobility_bonus)
                    
                    if color == PLAYER1_COLOR:
                        red_score += total_value
                        red_stack_power += stack_size * stack_size  # Quadratic for stack power
                        red_mobility += mobility_bonus
                        red_threats += threat_penalty
                    else:
                        white_score += total_value
                        white_stack_power += stack_size * stack_size
                        white_mobility += mobility_bonus
                        white_threats += threat_penalty
        
        # Strategic bonuses
        # Material advantage bonus
        material_diff = red_material - white_material
        material_bonus = material_diff * 3
        
        # Stack power advantage
        stack_power_diff = red_stack_power - white_stack_power
        stack_bonus = stack_power_diff * 0.5
        
        # Mobility advantage
        mobility_diff = red_mobility - white_mobility
        mobility_bonus = mobility_diff * 0.8
        
        # Threat advantage (negative because threats are penalties)
        threat_diff = white_threats - red_threats  # Lower threats for us is better
        threat_bonus = threat_diff * 2
        
        # Endgame consideration - encourage trading when ahead
        total_pieces = self.red_left + self.white_left
        if total_pieces <= 8:  # Endgame
            if red_material > white_material:
                # Encourage simplification when ahead
                endgame_bonus = (red_material - white_material) * 2
            else:
                # Avoid trades when behind
                endgame_bonus = (white_material - red_material) * -1
        else:
            endgame_bonus = 0
        
        # Final score calculation
        final_score = (red_score - white_score + 
                      material_bonus + stack_bonus + 
                      mobility_bonus + threat_bonus + 
                      endgame_bonus)
        
        return final_score
    
    def _calculate_position_bonus(self, row, col, color, is_king, stack_size):
        """Calculate positional bonus for a piece"""
        bonus = 0
        
        # Center control bonus
        center_rows = range(self.rows // 4, 3 * self.rows // 4)
        center_cols = range(self.cols // 4, 3 * self.cols // 4)
        
        if row in center_rows and col in center_cols:
            bonus += 3 * stack_size
        
        # Advancement bonus for non-kings
        if not is_king:
            if color == PLAYER1_COLOR:
                # Red moves toward row 0
                advancement = (self.rows - 1 - row) / (self.rows - 1)
                bonus += advancement * 8 * stack_size
            else:
                # White moves toward last row
                advancement = row / (self.rows - 1)
                bonus += advancement * 8 * stack_size
        else:
            # Kings are valuable everywhere but especially in center
            if row in center_rows and col in center_cols:
                bonus += 5 * stack_size
        
        # Back row protection for strong stacks
        if stack_size >= 2:
            if (color == PLAYER1_COLOR and row >= self.rows - 2) or \
               (color == PLAYER2_COLOR and row <= 1):
                bonus += 6
        
        return bonus
    
    def _calculate_threat_penalty(self, row, col, color, stack_size):
        """Calculate threat penalty for a piece (how vulnerable it is)"""
        penalty = 0
        opponent_color = PLAYER2_COLOR if color == PLAYER1_COLOR else PLAYER1_COLOR
        
        # Check if this piece can be captured by opponent
        for opp_row in range(self.rows):
            for opp_col in range(self.cols):
                opp_stack = self.get_stack(opp_row, opp_col)
                if opp_stack and len(opp_stack) > 0 and opp_stack[0].color == opponent_color:
                    opp_piece = opp_stack[0]
                    valid_moves = self.get_valid_moves(opp_piece)
                    
                    for move_pos, captured_pieces in valid_moves.items():
                        if (row, col) in [(p.row, p.col) for p in captured_pieces]:
                            # This piece is under threat!
                            threat_severity = len(opp_stack) / stack_size
                            penalty += 15 * threat_severity
        
        # Additional penalty for isolated pieces
        friendly_neighbors = 0
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                neighbor_stack = self.get_stack(nr, nc)
                if neighbor_stack and len(neighbor_stack) > 0 and neighbor_stack[0].color == color:
                    friendly_neighbors += 1
        
        if friendly_neighbors == 0:
            penalty += 5  # Isolated piece penalty
        
        return penalty
    
    def _calculate_mobility_bonus(self, row, col, color, stack_size):
        """Calculate mobility bonus for a piece"""
        piece = self.get_piece(row, col)
        if not piece:
            return 0
        
        valid_moves = self.get_valid_moves(piece)
        mobility = len(valid_moves)
        
        # Bonus for having multiple move options
        mobility_bonus = mobility * 2 * stack_size
        
        # Extra bonus for capture moves
        capture_moves = sum(1 for captured in valid_moves.values() if len(captured) > 0)
        mobility_bonus += capture_moves * 10 * stack_size
        
        return mobility_bonus
    
    def is_position_safe(self, row, col, color):
        """Check if a position is safe from immediate capture"""
        opponent_color = PLAYER2_COLOR if color == PLAYER1_COLOR else PLAYER1_COLOR
        
        for opp_row in range(self.rows):
            for opp_col in range(self.cols):
                opp_stack = self.get_stack(opp_row, opp_col)
                if opp_stack and len(opp_stack) > 0 and opp_stack[0].color == opponent_color:
                    opp_piece = opp_stack[0]
                    valid_moves = self.get_valid_moves(opp_piece)
                    
                    for move_pos, captured_pieces in valid_moves.items():
                        if (row, col) in [(p.row, p.col) for p in captured_pieces]:
                            return False  # Position is under threat
        
        return True  # Position is safe
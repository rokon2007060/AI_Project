"""
Advanced AI Agents for Checkers with Strategic Planning and Threat Awareness
"""
import copy
import time
import random
import math
from abc import ABC, abstractmethod
from constants import PLAYER1_COLOR, PLAYER2_COLOR, AI_TIME_LIMIT, AI_DEPTH_MINIMAX, AI_DEPTH_BACKTRACK, AI_DEPTH_FUZZY

class BaseAI(ABC):
    """Abstract base class for all AI agents"""
    
    def __init__(self, color, depth=3):
        self.color = color
        self.depth = depth
        self.nodes_expanded = 0
        self.evaluation_time = 0
        self.last_move_stats = {}
    
    @abstractmethod
    def get_move(self, board, game):
        pass
    
    def reset_stats(self):
        self.nodes_expanded = 0
        self.evaluation_time = 0
        self.last_move_stats = {}


class MinimaxBacktrackAgent(BaseAI):
    """
    Enhanced AI Agent 1: Strategic Minimax with Backtracking using MRV & LCV
    Features:
    - Threat-aware evaluation
    - Multi-ply lookahead
    - Positional strategy
    - Safe move prioritization
    """
    
    def __init__(self, color, depth=AI_DEPTH_BACKTRACK):
        super().__init__(color, depth)
        self.use_roulette = True
        self.minimax_weight = 0.7
        self.backtrack_weight = 0.3
        self.time_limit = AI_TIME_LIMIT
    
    def get_move(self, board, game):
        """Get move using strategic planning with threat awareness"""
        self.reset_stats()
        start_time = time.time()
        
        # Roulette wheel selection between strategies
        strategy = self._roulette_wheel_selection()
        
        if strategy == "minimax":
            result = self._get_strategic_minimax_move(board, game, start_time)
        else:
            result = self._get_enhanced_backtrack_move(board, game)
        
        self.evaluation_time = time.time() - start_time
        self.last_move_stats = {
            'nodes_expanded': self.nodes_expanded,
            'time': self.evaluation_time,
            'strategy': strategy,
            'agent': 'MinimaxBacktrack'
        }
        
        return result
    
    def _roulette_wheel_selection(self):
        """Select strategy using roulette wheel based on weights"""
        r = random.random()
        if r < self.minimax_weight:
            return "minimax"
        else:
            return "backtracking"
    
    def _get_strategic_minimax_move(self, board, game, start_time):
        """Get move using strategic minimax with threat awareness"""
        is_max = (self.color == PLAYER1_COLOR)
        
        # Use iterative deepening with time limit
        best_move = None
        best_move_info = None
        best_capture = False
        
        for current_depth in range(1, self.depth + 1):
            if time.time() - start_time > self.time_limit:
                break
                
            value, new_board, move_info, was_capture = self._strategic_minimax(
                board, current_depth, float('-inf'), float('inf'), is_max, game, start_time
            )
            
            if new_board is not None:
                best_move = new_board
                best_move_info = move_info
                best_capture = was_capture
        
        return best_move, best_move_info, best_capture
    
    def _strategic_minimax(self, position, depth, alpha, beta, max_player, game, start_time, original_depth=None):
        """
        Strategic minimax with enhanced evaluation and threat detection
        """
        if original_depth is None:
            original_depth = depth
            
        self.nodes_expanded += 1
        
        # Time limit check
        if time.time() - start_time > self.time_limit and depth < original_depth:
            return position.evaluate(), position, None, False
        
        # Terminal conditions
        if depth == 0 or position.winner() is not None:
            eval_score = self._strategic_evaluate(position, depth, original_depth)
            return eval_score, position, None, False
        
        color = PLAYER1_COLOR if max_player else PLAYER2_COLOR
        moves = self._get_strategic_moves(position, color, game)
        
        if not moves:
            penalty = 1000 if max_player else -1000
            return self._strategic_evaluate(position, depth, original_depth) - penalty, position, None, False
        
        if max_player:
            max_eval = float('-inf')
            best_move = None
            best_move_info = None
            best_capture = False
            
            for move_board, move_info, was_capture in moves:
                evaluation = self._strategic_minimax(
                    move_board, depth - 1, alpha, beta, False, game, start_time, original_depth
                )[0]
                
                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = move_board
                    best_move_info = move_info
                    best_capture = was_capture
                
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            
            return max_eval, best_move, best_move_info, best_capture
        else:
            min_eval = float('inf')
            best_move = None
            best_move_info = None
            best_capture = False
            
            for move_board, move_info, was_capture in moves:
                evaluation = self._strategic_minimax(
                    move_board, depth - 1, alpha, beta, True, game, start_time, original_depth
                )[0]
                
                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = move_board
                    best_move_info = move_info
                    best_capture = was_capture
                
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            
            return min_eval, best_move, best_move_info, best_capture
    
    def _strategic_evaluate(self, board, depth, original_depth):
        """
        Enhanced strategic evaluation considering:
        - Material advantage
        - Positional strength
        - Threat levels
        - King safety
        - Endgame considerations
        """
        base_score = board.evaluate()
        
        # Depth bonus - prefer quicker wins
        depth_bonus = (original_depth - depth) * 5
        
        # Threat assessment
        threat_score = self._calculate_threat_level(board)
        
        # Strategic positioning
        positional_score = self._calculate_positional_advantage(board)
        
        # Combine scores
        final_score = base_score + depth_bonus + threat_score + positional_score
        
        return final_score
    
    def _calculate_threat_level(self, board):
        """
        Calculate threat level for current player
        Enhanced to consider actual capture opportunities, not just piece safety
        """
        threat_score = 0
        my_color = self.color
        opponent_color = PLAYER2_COLOR if my_color == PLAYER1_COLOR else PLAYER1_COLOR
        
        # Count actual capture opportunities against opponent
        my_captures = 0
        for piece in board.get_all_pieces(my_color):
            capture_moves = board._get_capture_moves(piece)
            if capture_moves:
                # Count how many pieces would be captured
                for dest, captured_pieces in capture_moves.items():
                    my_captures += len(captured_pieces)
                    threat_score += len(captured_pieces) * 12  # Strong bonus for capture opportunities
        
        # Count opponent's capture opportunities (threats against us)
        opponent_captures = 0
        for piece in board.get_all_pieces(opponent_color):
            capture_moves = board._get_capture_moves(piece)
            if capture_moves:
                for dest, captured_pieces in capture_moves.items():
                    opponent_captures += len(captured_pieces)
                    threat_score -= len(captured_pieces) * 18  # Heavy penalty for being capturable
        
        # Count general positional threats (pieces that could be captured next turn)
        for piece in board.get_all_pieces(opponent_color):
            row, col = piece.row, piece.col
            if not board.is_position_safe(row, col, opponent_color):
                threat_score += 8  # Bonus for threatening opponent position
        
        for piece in board.get_all_pieces(my_color):
            row, col = piece.row, piece.col
            if not board.is_position_safe(row, col, my_color):
                threat_score -= 12  # Penalty for unsafe position
        
        return threat_score
    
    def _calculate_positional_advantage(self, board):
        """Calculate positional advantage"""
        positional_score = 0
        my_color = self.color
        
        # Control of center
        center_rows = range(board.rows // 4, 3 * board.rows // 4)
        center_cols = range(board.cols // 4, 3 * board.cols // 4)
        
        for piece in board.get_all_pieces(my_color):
            if piece.row in center_rows and piece.col in center_cols:
                positional_score += 3
        
        # King mobility in endgame
        if board.red_left + board.white_left <= 8:
            kings = [p for p in board.get_all_pieces(my_color) if p.king]
            for king in kings:
                # Kings should be mobile in endgame
                mobility = len(board.get_valid_moves(king))
                positional_score += mobility * 2
        
        return positional_score
    
    def _get_strategic_moves(self, board, color, game):
        """Get moves with strategic ordering"""
        moves_with_scores = []
        
        for piece in board.get_all_pieces(color):
            valid_moves = board.get_valid_moves(piece)
            
            for move, captured_pieces in valid_moves.items():
                temp_board = copy.deepcopy(board)
                temp_piece = temp_board.get_piece(piece.row, piece.col)
                
                if temp_piece:
                    from_pos = (temp_piece.row, temp_piece.col)
                    temp_board.move(temp_piece, move[0], move[1])
                    
                    was_capture = False
                    if captured_pieces and len(captured_pieces) > 0:
                        temp_board.remove(captured_pieces)
                        was_capture = True
                    
                    # Strategic move scoring
                    move_score = self._score_move_strategically(
                        board, temp_board, from_pos, move, was_capture, len(captured_pieces)
                    )
                    
                    move_info = (from_pos, move)
                    moves_with_scores.append((temp_board, move_info, was_capture, move_score))
        
        # Sort by strategic score (highest first for max player)
        moves_with_scores.sort(key=lambda x: x[3], reverse=(color == self.color))
        
        return [m[:3] for m in moves_with_scores]  # Remove score for compatibility
    
    def _score_move_strategically(self, old_board, new_board, from_pos, to_pos, was_capture, num_captured):
        """
        Score a move based on strategic considerations
        Enhanced to heavily favor multi-jump captures
        """
        score = 0
        
        # Capture bonus - HEAVILY favor multi-captures
        if was_capture:
            if num_captured >= 3:
                score += num_captured * 60  # Triple+ captures are massive
            elif num_captured == 2:
                score += num_captured * 45  # Double captures very strong
            else:
                score += num_captured * 30  # Single captures good
        
        # Promotion bonus
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = new_board.get_piece(to_row, to_col)
        if piece and not piece.king:
            if (piece.color == PLAYER1_COLOR and to_row == 0) or \
               (piece.color == PLAYER2_COLOR and to_row == new_board.rows - 1):
                score += 35  # Promotion is very valuable
        
        # Stacking bonus
        new_stack_size = new_board.get_stack_size(to_row, to_col)
        if new_stack_size > 1:
            score += new_stack_size * 10
        
        # Safety consideration
        if piece and new_board.is_position_safe(to_row, to_col, piece.color):
            score += 12
        elif piece:
            score -= 15  # Penalty for moving to unsafe position
        
        # Center control bonus
        center_rows = range(new_board.rows // 4, 3 * new_board.rows // 4)
        center_cols = range(new_board.cols // 4, 3 * new_board.cols // 4)
        
        if to_row in center_rows and to_col in center_cols:
            score += 5
        
        return score
    
    def _get_enhanced_backtrack_move(self, board, game):
        """Enhanced backtracking with strategic MRV/LCV"""
        # MRV: Select piece with fewest SAFE legal moves
        pieces = board.get_all_pieces(self.color)
        
        if not pieces:
            return None, None, False
        
        # Calculate safe legal moves for each piece
        piece_moves = []
        for piece in pieces:
            moves = board.get_valid_moves(piece)
            safe_moves = []
            
            for move, captured_pieces in moves.items():
                # Check if move is safe
                temp_board = copy.deepcopy(board)
                temp_piece = temp_board.get_piece(piece.row, piece.col)
                
                if temp_piece:
                    temp_board.move(temp_piece, move[0], move[1])
                    if captured_pieces:
                        temp_board.remove(captured_pieces)
                    
                    # Check if new position is safe
                    if board.is_position_safe(move[0], move[1], self.color):
                        safe_moves.append((move, captured_pieces))
            
            if safe_moves:
                piece_moves.append((piece, safe_moves, len(safe_moves)))
        
        if not piece_moves:
            # No safe moves, use all moves
            for piece in pieces:
                moves = board.get_valid_moves(piece)
                if moves:
                    piece_moves.append((piece, list(moves.items()), len(moves)))
        
        if not piece_moves:
            return None, None, False
        
        # Sort by number of safe moves (MRV)
        piece_moves.sort(key=lambda x: x[2])
        
        # Select piece with fewest safe moves
        selected_piece, valid_moves, _ = piece_moves[0]
        
        # LCV: Choose move that gives opponent least mobility
        best_move = None
        best_score = float('-inf')
        
        for move, captured_pieces in valid_moves:
            temp_board = copy.deepcopy(board)
            temp_piece = temp_board.get_piece(selected_piece.row, selected_piece.col)
            
            if temp_piece:
                from_pos = (temp_piece.row, temp_piece.col)
                temp_board.move(temp_piece, move[0], move[1])
                
                was_capture = False
                if captured_pieces and len(captured_pieces) > 0:
                    temp_board.remove(captured_pieces)
                    was_capture = True
                
                # Score based on opponent's constrained mobility
                opponent_color = PLAYER2_COLOR if self.color == PLAYER1_COLOR else PLAYER1_COLOR
                opponent_mobility = self._calculate_mobility(temp_board, opponent_color)
                
                # Strategic scoring
                score = -opponent_mobility  # Lower opponent mobility is better
                
                # Add bonuses
                if was_capture:
                    score += len(captured_pieces) * 20
                if temp_board.is_position_safe(move[0], move[1], self.color):
                    score += 15
                if (move[0] == 0 or move[0] == board.rows - 1) and not temp_piece.king:
                    score += 25  # Promotion bonus
                
                if score > best_score:
                    best_score = score
                    move_info = (from_pos, move)
                    best_move = (temp_board, move_info, was_capture)
        
        return best_move
    
    def _calculate_mobility(self, board, color):
        """Calculate total mobility for a color"""
        mobility = 0
        for piece in board.get_all_pieces(color):
            mobility += len(board.get_valid_moves(piece))
        return mobility


class MinimaxFuzzyAgent(BaseAI):
    """
    Enhanced AI Agent 2: Strategic Minimax with Advanced Fuzzy Logic
    Features:
    - Fuzzy threat assessment
    - Adaptive strategy based on game phase
    - Multi-criteria decision making
    - Risk-aware move selection
    """
    
    def __init__(self, color, depth=AI_DEPTH_FUZZY):
        super().__init__(color, depth)
        self.use_roulette = True
        self.minimax_weight = 0.6
        self.fuzzy_weight = 0.4
        self.fuzzy_evaluator = AdvancedFuzzyEvaluator()
        self.time_limit = AI_TIME_LIMIT
        self.game_phase = "midgame"  # opening, midgame, endgame
    
    def get_move(self, board, game):
        """Get move using strategic fuzzy logic with adaptive planning"""
        self.reset_stats()
        start_time = time.time()
        
        # Update game phase
        self._update_game_phase(board)
        
        # Roulette wheel selection
        strategy = self._adaptive_roulette_selection(board)
        
        if strategy == "minimax":
            result = self._get_adaptive_minimax_move(board, game, start_time)
        else:
            result = self._get_advanced_fuzzy_move(board, game, start_time)
        
        self.evaluation_time = time.time() - start_time
        self.last_move_stats = {
            'nodes_expanded': self.nodes_expanded,
            'time': self.evaluation_time,
            'strategy': strategy,
            'phase': self.game_phase,
            'agent': 'MinimaxFuzzy'
        }
        
        return result
    
    def _update_game_phase(self, board):
        """Update game phase based on board state"""
        total_pieces = board.red_left + board.white_left
        if total_pieces >= 20:
            self.game_phase = "opening"
        elif total_pieces >= 10:
            self.game_phase = "midgame"
        else:
            self.game_phase = "endgame"
    
    def _adaptive_roulette_selection(self, board):
        """Adaptive strategy selection based on game phase"""
        if self.game_phase == "opening":
            # Prefer minimax in opening for solid play
            self.minimax_weight = 0.7
            self.fuzzy_weight = 0.3
        elif self.game_phase == "endgame":
            # Prefer fuzzy in endgame for creative solutions
            self.minimax_weight = 0.4
            self.fuzzy_weight = 0.6
        else:
            # Balanced in midgame
            self.minimax_weight = 0.6
            self.fuzzy_weight = 0.4
        
        r = random.random()
        if r < self.minimax_weight:
            return "minimax"
        else:
            return "fuzzy"
    
    def _get_adaptive_minimax_move(self, board, game, start_time):
        """Adaptive minimax that adjusts strategy based on game phase"""
        is_max = (self.color == PLAYER1_COLOR)
        
        best_move = None
        best_move_info = None
        best_capture = False
        
        # Adjust depth based on game phase
        adaptive_depth = self.depth
        if self.game_phase == "endgame":
            adaptive_depth += 1  # Deeper search in endgame
        
        for current_depth in range(1, adaptive_depth + 1):
            if time.time() - start_time > self.time_limit:
                break
                
            value, new_board, move_info, was_capture = self._adaptive_minimax(
                board, current_depth, float('-inf'), float('inf'), is_max, game, start_time
            )
            
            if new_board is not None:
                best_move = new_board
                best_move_info = move_info
                best_capture = was_capture
        
        return best_move, best_move_info, best_capture
    
    def _adaptive_minimax(self, position, depth, alpha, beta, max_player, game, start_time):
        """Adaptive minimax with phase-aware evaluation"""
        self.nodes_expanded += 1
        
        # Time limit check
        if time.time() - start_time > self.time_limit:
            return position.evaluate(), position, None, False
        
        if depth == 0 or position.winner() is not None:
            eval_score = self._phase_aware_evaluate(position)
            return eval_score, position, None, False
        
        color = PLAYER1_COLOR if max_player else PLAYER2_COLOR
        moves = self._get_phase_aware_moves(position, color, game)
        
        if not moves:
            penalty = 1000 if max_player else -1000
            return self._phase_aware_evaluate(position) - penalty, position, None, False
        
        if max_player:
            max_eval = float('-inf')
            best_move = None
            best_move_info = None
            best_capture = False
            
            for move_board, move_info, was_capture in moves:
                evaluation = self._adaptive_minimax(
                    move_board, depth - 1, alpha, beta, False, game, start_time
                )[0]
                
                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = move_board
                    best_move_info = move_info
                    best_capture = was_capture
                
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            
            return max_eval, best_move, best_move_info, best_capture
        else:
            min_eval = float('inf')
            best_move = None
            best_move_info = None
            best_capture = False
            
            for move_board, move_info, was_capture in moves:
                evaluation = self._adaptive_minimax(
                    move_board, depth - 1, alpha, beta, True, game, start_time
                )[0]
                
                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = move_board
                    best_move_info = move_info
                    best_capture = was_capture
                
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            
            return min_eval, best_move, best_move_info, best_capture
    
    def _phase_aware_evaluate(self, board):
        """Evaluation that adapts to game phase"""
        base_score = board.evaluate()
        
        # Phase-specific adjustments
        if self.game_phase == "opening":
            # Focus on development and center control
            development_bonus = self._calculate_development_score(board)
            base_score += development_bonus
        elif self.game_phase == "endgame":
            # Focus on king activity and passed pieces
            endgame_bonus = self._calculate_endgame_score(board)
            base_score += endgame_bonus
        
        return base_score
    
    def _calculate_development_score(self, board):
        """Calculate development score for opening phase"""
        score = 0
        my_color = self.color
        
        # Bonus for moving pieces from back rank
        for piece in board.get_all_pieces(my_color):
            if not piece.king:
                if my_color == PLAYER1_COLOR and piece.row < board.rows - 3:
                    score += 2  # Red pieces moving up
                elif my_color == PLAYER2_COLOR and piece.row > 2:
                    score += 2  # White pieces moving down
        
        return score
    
    def _calculate_endgame_score(self, board):
        """Calculate endgame-specific score"""
        score = 0
        my_color = self.color
        opponent_color = PLAYER2_COLOR if my_color == PLAYER1_COLOR else PLAYER1_COLOR
        
        # King activity bonus
        my_kings = [p for p in board.get_all_pieces(my_color) if p.king]
        opp_kings = [p for p in board.get_all_pieces(opponent_color) if p.king]
        
        for king in my_kings:
            # Kings should be active in endgame
            mobility = len(board.get_valid_moves(king))
            score += mobility * 3
        
        # Passed piece bonus (pieces close to promotion)
        for piece in board.get_all_pieces(my_color):
            if not piece.king:
                if my_color == PLAYER1_COLOR and piece.row <= 2:
                    score += 8  # Red close to promotion
                elif my_color == PLAYER2_COLOR and piece.row >= board.rows - 3:
                    score += 8  # White close to promotion
        
        return score
    
    def _get_phase_aware_moves(self, board, color, game):
        """Get moves with phase-aware ordering"""
        moves_with_scores = []
        
        for piece in board.get_all_pieces(color):
            valid_moves = board.get_valid_moves(piece)
            
            for move, captured_pieces in valid_moves.items():
                temp_board = copy.deepcopy(board)
                temp_piece = temp_board.get_piece(piece.row, piece.col)
                
                if temp_piece:
                    from_pos = (temp_piece.row, temp_piece.col)
                    temp_board.move(temp_piece, move[0], move[1])
                    
                    was_capture = False
                    if captured_pieces and len(captured_pieces) > 0:
                        temp_board.remove(captured_pieces)
                        was_capture = True
                    
                    # Phase-aware move scoring
                    move_score = self._phase_aware_move_score(
                        board, temp_board, from_pos, move, was_capture, len(captured_pieces)
                    )
                    
                    move_info = (from_pos, move)
                    moves_with_scores.append((temp_board, move_info, was_capture, move_score))
        
        # Sort by phase-aware score
        moves_with_scores.sort(key=lambda x: x[3], reverse=(color == self.color))
        
        return [m[:3] for m in moves_with_scores]
    
    def _phase_aware_move_score(self, old_board, new_board, from_pos, to_pos, was_capture, num_captured):
        """Score move based on current game phase"""
        score = 0
        
        # Base bonuses (always good)
        if was_capture:
            score += num_captured * 25
        
        # Phase-specific scoring
        if self.game_phase == "opening":
            score += self._opening_move_score(old_board, new_board, from_pos, to_pos)
        elif self.game_phase == "midgame":
            score += self._midgame_move_score(old_board, new_board, from_pos, to_pos)
        else:  # endgame
            score += self._endgame_move_score(old_board, new_board, from_pos, to_pos)
        
        return score
    
    def _opening_move_score(self, old_board, new_board, from_pos, to_pos):
        """Opening phase move scoring"""
        score = 0
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Development bonus
        if self.color == PLAYER1_COLOR:
            if from_row > to_row:  # Moving upward (good for red)
                score += 5
        else:
            if from_row < to_row:  # Moving downward (good for white)
                score += 5
        
        # Center control in opening
        center_rows = range(new_board.rows // 4, 3 * new_board.rows // 4)
        center_cols = range(new_board.cols // 4, 3 * new_board.cols // 4)
        
        if to_row in center_rows and to_col in center_cols:
            score += 8
        
        return score
    
    def _midgame_move_score(self, old_board, new_board, from_pos, to_pos):
        """Midgame phase move scoring"""
        score = 0
        
        # Safety and threat considerations
        piece = new_board.get_piece(to_pos[0], to_pos[1])
        if piece and new_board.is_position_safe(to_pos[0], to_pos[1], piece.color):
            score += 10
        
        # Stack building
        new_stack_size = new_board.get_stack_size(to_pos[0], to_pos[1])
        if new_stack_size > 1:
            score += new_stack_size * 6
        
        return score
    
    def _endgame_move_score(self, old_board, new_board, from_pos, to_pos):
        """Endgame phase move scoring"""
        score = 0
        to_row, to_col = to_pos
        
        piece = new_board.get_piece(to_row, to_col)
        if piece:
            # King activity
            if piece.king:
                mobility = len(new_board.get_valid_moves(piece))
                score += mobility * 2
            
            # Promotion urgency
            if not piece.king:
                if (piece.color == PLAYER1_COLOR and to_row == 0) or \
                   (piece.color == PLAYER2_COLOR and to_row == new_board.rows - 1):
                    score += 40  # Very high bonus for promotion in endgame
        
        return score
    
    def _get_advanced_fuzzy_move(self, board, game, start_time):
        """Advanced fuzzy logic move selection"""
        moves_with_scores = []
        
        for piece in board.get_all_pieces(self.color):
            valid_moves = board.get_valid_moves(piece)
            
            for move, captured_pieces in valid_moves.items():
                temp_board = copy.deepcopy(board)
                temp_piece = temp_board.get_piece(piece.row, piece.col)
                
                if temp_piece:
                    from_pos = (temp_piece.row, temp_piece.col)
                    temp_board.move(temp_piece, move[0], move[1])
                    
                    was_capture = False
                    if captured_pieces and len(captured_pieces) > 0:
                        temp_board.remove(captured_pieces)
                        was_capture = True
                    
                    # Advanced fuzzy evaluation
                    fuzzy_score = self._advanced_fuzzy_evaluate(temp_board, from_pos, move, was_capture)
                    
                    move_info = (from_pos, move)
                    moves_with_scores.append((temp_board, move_info, was_capture, fuzzy_score))
        
        if not moves_with_scores:
            return None, None, False
        
        # Use fuzzy roulette selection
        best_move = self._fuzzy_roulette_selection(moves_with_scores)
        return best_move
    
    def _advanced_fuzzy_evaluate(self, board, from_pos, move, was_capture):
        """Advanced fuzzy evaluation considering multiple factors"""
        # Extract multiple game state features
        features = self._extract_fuzzy_features(board, from_pos, move, was_capture)
        
        # Use fuzzy evaluator
        score = self.fuzzy_evaluator.evaluate_advanced(features, self.game_phase)
        
        return score
    
    def _extract_fuzzy_features(self, board, from_pos, move, was_capture):
        """Extract features for fuzzy evaluation"""
        features = {}
        
        # Material features
        if self.color == PLAYER1_COLOR:
            features['material_balance'] = board.red_left - board.white_left
            features['king_balance'] = board.red_kings - board.white_kings
        else:
            features['material_balance'] = board.white_left - board.red_left
            features['king_balance'] = board.white_kings - board.red_kings
        
        # Positional features
        features['center_control'] = self._calculate_center_control(board)
        features['development'] = self._calculate_development(board)
        
        # Threat features
        features['threat_level'] = self._calculate_threat_level(board)
        features['safety_level'] = self._calculate_safety_level(board)
        
        # Move-specific features
        features['is_capture'] = 1 if was_capture else 0
        features['promotion_chance'] = self._calculate_promotion_chance(board, move)
        features['stack_potential'] = self._calculate_stack_potential(board, move)
        
        return features
    
    def _calculate_center_control(self, board):
        """Calculate center control metric"""
        my_center = 0
        opp_center = 0
        
        center_rows = range(board.rows // 4, 3 * board.rows // 4)
        center_cols = range(board.cols // 4, 3 * board.cols // 4)
        
        for row in center_rows:
            for col in center_cols:
                stack_color = board.get_stack_color(row, col)
                if stack_color == self.color:
                    my_center += 1
                elif stack_color is not None:
                    opp_center += 1
        
        return (my_center - opp_center) / max(1, my_center + opp_center)
    
    def _calculate_development(self, board):
        """Calculate development metric"""
        development = 0
        total_pieces = 0
        
        for piece in board.get_all_pieces(self.color):
            total_pieces += 1
            if self.color == PLAYER1_COLOR:
                development += (board.rows - 1 - piece.row)  # Red wants to move up
            else:
                development += piece.row  # White wants to move down
        
        return development / max(1, total_pieces * (board.rows - 1))
    
    def _calculate_threat_level(self, board):
        """Calculate threat level metric"""
        threats = 0
        total_pieces = 0
        
        for piece in board.get_all_pieces(self.color):
            total_pieces += 1
            if not board.is_position_safe(piece.row, piece.col, self.color):
                threats += 1
        
        return threats / max(1, total_pieces)
    
    def _calculate_safety_level(self, board):
        """Calculate safety level metric"""
        safe_positions = 0
        total_pieces = 0
        
        for piece in board.get_all_pieces(self.color):
            total_pieces += 1
            if board.is_position_safe(piece.row, piece.col, self.color):
                safe_positions += 1
        
        return safe_positions / max(1, total_pieces)
    
    def _calculate_promotion_chance(self, board, move):
        """Calculate promotion chance for move"""
        to_row, to_col = move
        
        if self.color == PLAYER1_COLOR and to_row == 0:
            return 1.0
        elif self.color == PLAYER2_COLOR and to_row == board.rows - 1:
            return 1.0
        
        # Estimate promotion chance based on distance
        if self.color == PLAYER1_COLOR:
            distance = to_row
        else:
            distance = board.rows - 1 - to_row
        
        return 1.0 - (distance / (board.rows - 1))
    
    def _calculate_stack_potential(self, board, move):
        """Calculate stack potential for move"""
        to_row, to_col = move
        current_stack = board.get_stack_size(to_row, to_col)
        
        if current_stack > 0 and board.get_stack_color(to_row, to_col) == self.color:
            # Joining existing stack
            return min(1.0, current_stack / 3.0)
        else:
            # Potential to build stack later
            return 0.3
    
    def _fuzzy_roulette_selection(self, moves_with_scores):
        """Fuzzy roulette wheel selection with normalization"""
        scores = [max(score, 0.1) for _, _, _, score in moves_with_scores]
        
        # Softmax normalization for better probability distribution
        exp_scores = [math.exp(score / 10) for score in scores]  # Temperature parameter 10
        total = sum(exp_scores)
        probabilities = [score / total for score in exp_scores]
        
        # Roulette wheel selection
        r = random.random()
        cumulative_prob = 0
        
        for i, prob in enumerate(probabilities):
            cumulative_prob += prob
            if r <= cumulative_prob:
                board, move_info, was_capture, _ = moves_with_scores[i]
                return board, move_info, was_capture
        
        # Fallback to best move
        best_idx = scores.index(max(scores))
        board, move_info, was_capture, _ = moves_with_scores[best_idx]
        return board, move_info, was_capture


class AdvancedFuzzyEvaluator:
    """
    Advanced Fuzzy Logic Evaluation System
    Uses multiple fuzzy rules adapted to game phases
    """
    
    def __init__(self):
        self.setup_membership_functions()
    
    def setup_membership_functions(self):
        """Setup advanced membership functions"""
        # Using simplified evaluation for demonstration
        # In a full implementation, this would have proper fuzzy sets and rules
        pass
    
    def evaluate_advanced(self, features, game_phase):
        """
        Advanced fuzzy evaluation with phase adaptation
        """
        score = 0
        
        # Material factors (always important)
        score += features['material_balance'] * 25
        score += features['king_balance'] * 15
        
        # Phase-adaptive weighting
        if game_phase == "opening":
            score += self._opening_evaluation(features)
        elif game_phase == "midgame":
            score += self._midgame_evaluation(features)
        else:  # endgame
            score += self._endgame_evaluation(features)
        
        # Move quality factors
        score += features['is_capture'] * 30
        score += features['promotion_chance'] * 25
        score += features['stack_potential'] * 12
        
        # Safety considerations
        score -= features['threat_level'] * 20
        score += features['safety_level'] * 15
        
        return score
    
    def _opening_evaluation(self, features):
        """Opening phase evaluation"""
        score = 0
        score += features['center_control'] * 20
        score += features['development'] * 15
        return score
    
    def _midgame_evaluation(self, features):
        """Midgame phase evaluation"""
        score = 0
        score += features['center_control'] * 15
        score += features['development'] * 10
        # More emphasis on threats and safety in midgame
        score -= features['threat_level'] * 25
        score += features['safety_level'] * 20
        return score
    
    def _endgame_evaluation(self, features):
        """Endgame phase evaluation"""
        score = 0
        # Less emphasis on center, more on king activity and promotion
        score += features['center_control'] * 8
        score += features['promotion_chance'] * 35
        return score


# For backward compatibility
FuzzyMinimaxAgent = MinimaxFuzzyAgent
HeuristicBacktrackAgent = MinimaxBacktrackAgent
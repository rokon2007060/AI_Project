"""
A* Search for Multi-Jump Capture Path Planning in Checkers
Finds optimal capture sequences for pieces/stacks
"""
import heapq
from typing import List, Tuple, Set, Optional

class CaptureNode:
    """
    Node in the A* search tree for capture planning
    Represents a state in a capture sequence
    """
    
    def __init__(self, position, captured_set, path, g_cost, h_cost, parent=None):
        """
        Initialize a capture node
        
        Args:
            position: Current (row, col) position
            captured_set: Set of captured piece positions so far
            path: List of positions taken to reach this node
            g_cost: Actual cost from start (number of jumps)
            h_cost: Heuristic estimated cost to complete captures
            parent: Parent node in search tree
        """
        self.position = position
        self.captured_set = frozenset(captured_set)  # Immutable for hashing
        self.path = path.copy()
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = g_cost + h_cost
        self.parent = parent
    
    def __lt__(self, other):
        """Compare nodes for priority queue (lower f_cost is better)"""
        if self.f_cost == other.f_cost:
            # Tie-breaker: prefer more captures
            return len(self.captured_set) > len(other.captured_set)
        return self.f_cost < other.f_cost
    
    def __eq__(self, other):
        """Check if two nodes represent the same state"""
        return (self.position == other.position and 
                self.captured_set == other.captured_set)
    
    def __hash__(self):
        """Hash for use in visited set"""
        return hash((self.position, self.captured_set))


class AStarCapturePlanner:
    """
    A* search planner for finding optimal capture sequences
    """
    
    def __init__(self, board, piece):
        """
        Initialize the capture planner
        
        Args:
            board: Current board state
            piece: Piece to plan captures for
        """
        self.board = board
        self.piece = piece
        self.start_pos = (piece.row, piece.col)
        self.color = piece.color
        self.is_king = piece.king
    
    def heuristic(self, position, captured_set, available_targets):
        """
        Heuristic function: estimate remaining captures possible
        
        Args:
            position: Current position
            captured_set: Set of already captured positions
            available_targets: Set of capturable enemy positions
        
        Returns:
            Estimated cost (number of remaining captures possible)
        """
        remaining_targets = available_targets - captured_set
        
        if not remaining_targets:
            return 0
        
        # Estimate based on Manhattan distance to nearest uncaptured enemy
        min_dist = float('inf')
        row, col = position
        
        for target_row, target_col in remaining_targets:
            # Manhattan distance (divided by 2 since we move diagonally)
            dist = (abs(row - target_row) + abs(col - target_col)) / 2
            min_dist = min(min_dist, dist)
        
        # Heuristic: assume we can capture remaining enemies
        # Weight by distance to encourage moving toward targets
        return min_dist * 0.5
    
    def get_capture_moves(self, position, captured_set):
        """
        Get possible capture moves from a position
        
        Args:
            position: Current (row, col)
            captured_set: Set of already captured positions
        
        Returns:
            List of (new_position, captured_position) tuples
        """
        from constants import ROWS, COLS, PLAYER1_COLOR, PLAYER2_COLOR
        
        row, col = position
        moves = []
        
        # Determine which directions this piece can move
        directions = []
        if self.color == PLAYER1_COLOR or self.is_king:
            # Can move up (negative row direction)
            directions.extend([(-1, -1), (-1, 1)])
        if self.color == PLAYER2_COLOR or self.is_king:
            # Can move down (positive row direction)
            directions.extend([(1, -1), (1, 1)])
        
        # Check each direction for captures
        for dr, dc in directions:
            # Position of potential enemy
            enemy_row, enemy_col = row + dr, col + dc
            
            # Position after jumping enemy
            land_row, land_col = row + 2 * dr, col + 2 * dc
            
            # Check if positions are valid
            if not (0 <= enemy_row < ROWS and 0 <= enemy_col < COLS):
                continue
            if not (0 <= land_row < ROWS and 0 <= land_col < COLS):
                continue
            
            # Check if we already captured this enemy
            if (enemy_row, enemy_col) in captured_set:
                continue
            
            # Check if there's an enemy at the jump position
            enemy_stack = self.board.get_stack(enemy_row, enemy_col)
            if not enemy_stack or len(enemy_stack) == 0:
                continue
            if enemy_stack[0].color == self.color:
                continue  # Friendly piece
            
            # Check if landing square is empty or was our starting position
            land_stack = self.board.get_stack(land_row, land_col)
            if land_stack and len(land_stack) > 0:
                if (land_row, land_col) != self.start_pos:
                    continue  # Occupied by another piece
            
            # Check if our stack can capture this enemy stack
            my_stack_size = self.board.get_stack_size(*self.start_pos)
            enemy_stack_size = len(enemy_stack)
            
            if my_stack_size >= enemy_stack_size:
                # Valid capture
                moves.append(((land_row, land_col), (enemy_row, enemy_col)))
        
        return moves
    
    def find_best_capture_sequence(self, max_iterations=1000):
        """
        Use A* to find the best capture sequence
        
        Args:
            max_iterations: Maximum search iterations to prevent infinite loops
        
        Returns:
            Tuple of (path, captured_positions) or (None, None) if no captures
        """
        # Find all capturable enemy positions
        available_targets = self.get_all_capturable_enemies()
        
        if not available_targets:
            return None, None  # No captures available
        
        # Initialize search
        start_node = CaptureNode(
            position=self.start_pos,
            captured_set=set(),
            path=[self.start_pos],
            g_cost=0,
            h_cost=self.heuristic(self.start_pos, set(), available_targets),
            parent=None
        )
        
        open_set = [start_node]
        closed_set = set()
        best_solution = None
        
        iterations = 0
        
        while open_set and iterations < max_iterations:
            iterations += 1
            
            # Get node with lowest f_cost
            current = heapq.heappop(open_set)
            
            # Check if this is better than our current best
            if best_solution is None or len(current.captured_set) > len(best_solution.captured_set):
                if len(current.captured_set) > 0:
                    best_solution = current
            
            # Check if we've visited this state
            if current in closed_set:
                continue
            closed_set.add(current)
            
            # Get possible capture moves from current position
            capture_moves = self.get_capture_moves(current.position, current.captured_set)
            
            # If no more captures possible, this is a terminal node
            if not capture_moves:
                if best_solution is None or len(current.captured_set) > len(best_solution.captured_set):
                    best_solution = current
                continue
            
            # Expand successors
            for new_pos, captured_pos in capture_moves:
                new_captured = set(current.captured_set)
                new_captured.add(captured_pos)
                
                new_path = current.path + [new_pos]
                new_g = current.g_cost + 1
                new_h = self.heuristic(new_pos, new_captured, available_targets)
                
                successor = CaptureNode(
                    position=new_pos,
                    captured_set=new_captured,
                    path=new_path,
                    g_cost=new_g,
                    h_cost=new_h,
                    parent=current
                )
                
                if successor not in closed_set:
                    heapq.heappush(open_set, successor)
        
        # Return best solution found
        if best_solution and len(best_solution.captured_set) > 0:
            return best_solution.path, list(best_solution.captured_set)
        
        return None, None
    
    def get_all_capturable_enemies(self):
        """
        Get all enemy positions that could potentially be captured
        
        Returns:
            Set of (row, col) positions of capturable enemies
        """
        from constants import ROWS, COLS, PLAYER1_COLOR, PLAYER2_COLOR
        
        enemy_color = PLAYER2_COLOR if self.color == PLAYER1_COLOR else PLAYER1_COLOR
        capturable = set()
        
        my_stack_size = self.board.get_stack_size(*self.start_pos)
        
        for row in range(ROWS):
            for col in range(COLS):
                stack = self.board.get_stack(row, col)
                if stack and len(stack) > 0:
                    if stack[0].color == enemy_color:
                        # Check if our stack can capture this enemy stack
                        enemy_stack_size = len(stack)
                        if my_stack_size >= enemy_stack_size:
                            capturable.add((row, col))
        
        return capturable


def plan_capture_sequence(board, piece):
    """
    Convenience function to plan a capture sequence for a piece
    
    Args:
        board: Current board state
        piece: Piece to plan for
    
    Returns:
        Tuple of (path, captured_positions) or (None, None)
    """
    planner = AStarCapturePlanner(board, piece)
    return planner.find_best_capture_sequence()


def evaluate_capture_opportunity(board, piece):
    """
    Evaluate how good a capture opportunity is for a piece
    
    Args:
        board: Current board state
        piece: Piece to evaluate
    
    Returns:
        Score indicating capture potential (higher is better)
    """
    planner = AStarCapturePlanner(board, piece)
    path, captured = planner.find_best_capture_sequence()
    
    if captured is None or len(captured) == 0:
        return 0
    
    # Score based on number of captures and stack sizes
    score = len(captured) * 10
    
    # Bonus for capturing larger stacks
    for cap_row, cap_col in captured:
        stack_size = board.get_stack_size(cap_row, cap_col)
        score += stack_size * 5
    
    return score

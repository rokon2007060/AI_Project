"""
AI Player with minimax algorithm for checkers
"""
import copy
from constants import PLAYER1_COLOR, PLAYER2_COLOR

def minimax(position, depth, max_player, game):
    """
    Minimax algorithm with alpha-beta pruning
    Returns (evaluation, best_move, last_move_info, was_capture)
    """
    if depth == 0 or position.winner() is not None:
        return position.evaluate(), position, None, False
    
    if max_player:
        max_eval = float('-inf')
        best_move = None
        best_move_info = None
        best_capture = False
        for move, move_info, was_capture in get_all_moves(position, PLAYER1_COLOR, game):
            evaluation = minimax(move, depth - 1, False, game)[0]
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
                best_move_info = move_info
                best_capture = was_capture
        
        return max_eval, best_move, best_move_info, best_capture
    else:
        min_eval = float('inf')
        best_move = None
        best_move_info = None
        best_capture = False
        for move, move_info, was_capture in get_all_moves(position, PLAYER2_COLOR, game):
            evaluation = minimax(move, depth - 1, True, game)[0]
            if evaluation < min_eval:
                min_eval = evaluation
                best_move = move
                best_move_info = move_info
                best_capture = was_capture
        
        return min_eval, best_move, best_move_info, best_capture


def minimax_alpha_beta(position, depth, alpha, beta, max_player, game):
    """
    Minimax algorithm with alpha-beta pruning (optimized)
    Returns (evaluation, best_move, last_move_info, was_capture)
    """
    if depth == 0 or position.winner() is not None:
        return position.evaluate(), position, None, False
    
    if max_player:
        max_eval = float('-inf')
        best_move = None
        best_move_info = None
        best_capture = False
        moves = get_all_moves(position, PLAYER1_COLOR, game)
        
        # If no moves available, return current position
        if not moves:
            return position.evaluate(), position, None, False
        
        for move, move_info, was_capture in moves:
            evaluation = minimax_alpha_beta(move, depth - 1, alpha, beta, False, game)[0]
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
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
        moves = get_all_moves(position, PLAYER2_COLOR, game)
        
        # If no moves available, return current position
        if not moves:
            return position.evaluate(), position, None, False
        
        for move, move_info, was_capture in moves:
            evaluation = minimax_alpha_beta(move, depth - 1, alpha, beta, True, game)[0]
            if evaluation < min_eval:
                min_eval = evaluation
                best_move = move
                best_move_info = move_info
                best_capture = was_capture
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        
        return min_eval, best_move, best_move_info, best_capture


def simulate_move(piece, move, board, game, skip):
    """Simulate a move and return new board state"""
    from_pos = (piece.row, piece.col)
    board.move(piece, move[0], move[1])
    
    was_capture = False
    if skip:
        board.remove(skip)
        was_capture = True
    
    to_pos = (move[0], move[1])
    return board, (from_pos, to_pos), was_capture


def get_all_moves(board, color, game):
    """Get all possible moves for a color"""
    moves = []
    
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            temp_board = copy.deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            if temp_piece is not None:
                new_board, last_move, was_capture = simulate_move(temp_piece, move, temp_board, game, skip)
                moves.append((new_board, last_move, was_capture))
    
    return moves


def get_best_move(board, color, depth=3, use_alpha_beta=True):
    """
    Get the best move for AI
    
    Args:
        board: Current board state
        color: Color of AI player
        depth: Search depth (higher = smarter but slower)
        use_alpha_beta: Use alpha-beta pruning optimization
    
    Returns:
        (best_board, last_move, was_capture): Board state after best move, move info, and capture flag
    """
    if use_alpha_beta:
        if color == PLAYER1_COLOR:
            value, new_board, move_info, was_capture = minimax_alpha_beta(board, depth, float('-inf'), float('inf'), True, None)
        else:
            value, new_board, move_info, was_capture = minimax_alpha_beta(board, depth, float('-inf'), float('inf'), False, None)
    else:
        if color == PLAYER1_COLOR:
            value, new_board, move_info, was_capture = minimax(board, depth, True, None)
        else:
            value, new_board, move_info, was_capture = minimax(board, depth, False, None)
    
    return new_board, move_info, was_capture


"""
Stack class for representing stacked pieces in Checkers with piece pairing
Supports up to 3 pieces per stack
"""
from piece import Piece

class Stack:
    MAX_HEIGHT = 3
    
    def __init__(self, pieces=None):
        """
        Initialize a stack with optional initial pieces
        
        Args:
            pieces: List of Piece objects (max 3)
        """
        self.pieces = pieces if pieces else []
        if len(self.pieces) > self.MAX_HEIGHT:
            raise ValueError(f"Stack cannot exceed {self.MAX_HEIGHT} pieces")
    
    @property
    def height(self):
        """Get the height of the stack"""
        return len(self.pieces)
    
    @property
    def color(self):
        """Get the color of the stack (color of bottom piece)"""
        if self.is_empty():
            return None
        return self.pieces[0].color
    
    @property
    def top_piece(self):
        """Get the top piece of the stack"""
        if self.is_empty():
            return None
        return self.pieces[0]
    
    @property
    def is_king(self):
        """Check if top piece is a king"""
        if self.is_empty():
            return False
        return self.pieces[0].king
    
    def is_empty(self):
        """Check if stack is empty"""
        return len(self.pieces) == 0
    
    def is_full(self):
        """Check if stack is at maximum capacity"""
        return len(self.pieces) >= self.MAX_HEIGHT
    
    def can_add_piece(self, piece=None):
        """
        Check if a piece can be added to this stack
        
        Args:
            piece: Piece to add (optional, checks if space available)
        
        Returns:
            True if piece can be added, False otherwise
        """
        if self.is_full():
            return False
        if piece and not self.is_empty():
            # Can only stack pieces of the same color
            if piece.color != self.color:
                return False
        return True
    
    def add_piece(self, piece):
        """
        Add a piece to the stack
        
        Args:
            piece: Piece object to add
        
        Returns:
            True if successful, False otherwise
        """
        if not self.can_add_piece(piece):
            return False
        
        # Add to the top (index 0)
        self.pieces.insert(0, piece)
        return True
    
    def remove_top_piece(self):
        """
        Remove and return the top piece from the stack
        
        Returns:
            Piece object or None if stack is empty
        """
        if self.is_empty():
            return None
        return self.pieces.pop(0)
    
    def remove_all_pieces(self):
        """
        Remove all pieces from the stack (for capture)
        
        Returns:
            List of all pieces that were in the stack
        """
        captured = self.pieces.copy()
        self.pieces = []
        return captured
    
    def can_capture(self, enemy_stack):
        """
        Check if this stack can capture an enemy stack
        Rule: Attacker stack height must be >= defender stack height
        
        Args:
            enemy_stack: Stack object to potentially capture
        
        Returns:
            True if can capture, False otherwise
        """
        if enemy_stack.is_empty():
            return False
        if self.is_empty():
            return False
        if self.color == enemy_stack.color:
            return False
        
        # Can capture if attacker height >= defender height
        return self.height >= enemy_stack.height
    
    def get_strength(self):
        """
        Get the combat strength of this stack
        Used for evaluation and capture rules
        
        Returns:
            Integer strength value
        """
        if self.is_empty():
            return 0
        
        strength = self.height
        
        # King bonus
        if self.is_king:
            strength += 0.5
        
        return strength
    
    def make_king(self):
        """Promote the top piece to king"""
        if not self.is_empty() and not self.pieces[0].king:
            self.pieces[0].make_king()
    
    def copy(self):
        """
        Create a deep copy of this stack
        
        Returns:
            New Stack object with copied pieces
        """
        import copy
        new_pieces = [copy.copy(piece) for piece in self.pieces]
        return Stack(new_pieces)
    
    def __repr__(self):
        """String representation of the stack"""
        if self.is_empty():
            return "Stack(empty)"
        color_str = "RED" if self.pieces[0].color == (255, 0, 0) else "WHITE"
        king_str = "K" if self.is_king else "N"
        return f"Stack({color_str}, height={self.height}, top={king_str})"
    
    def __len__(self):
        """Allow len() to work on Stack"""
        return self.height
    
    def __bool__(self):
        """Allow boolean evaluation (True if not empty)"""
        return not self.is_empty()

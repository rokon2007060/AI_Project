"""
Piece class for checkers game
"""
import pygame
from constants import SQUARE_SIZE, GREY, GOLD, CROWN, BLACK, WHITE

class Piece:
    PADDING = 15
    BORDER = 2
    
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()
    
    def calc_pos(self):
        """Calculate pixel position from row/col"""
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2
    
    def make_king(self):
        """Promote piece to king"""
        self.king = True
    
    def draw(self, win, stack_size=1):
        """Draw the piece on the board with stack indicator"""
        radius = SQUARE_SIZE // 2 - self.PADDING
        
        # Draw border
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.BORDER)
        # Draw main piece
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        
        # Draw stack number if stacked (2 or 3)
        if stack_size > 1:
            font_size = max(20, SQUARE_SIZE // 3)
            font = pygame.font.SysFont('arial', font_size, bold=True)
            
            # Use contrasting text color
            if self.color == WHITE:
                text_color = BLACK
            else:
                text_color = WHITE
                
            stack_text = font.render(str(stack_size), True, text_color)
            text_rect = stack_text.get_rect(center=(self.x, self.y))
            win.blit(stack_text, text_rect)
        
        # Draw crown for kings
        if self.king:
            crown_font_size = max(24, SQUARE_SIZE // 2)
            crown_font = pygame.font.SysFont('arial', crown_font_size, bold=True)
            crown_text = crown_font.render(CROWN, True, GOLD)
            crown_rect = crown_text.get_rect(center=(self.x, self.y))
            win.blit(crown_text, crown_rect)
    
    def move(self, row, col):
        """Move piece to new position"""
        self.row = row
        self.col = col
        self.calc_pos()
    
    def __repr__(self):
        return f"Piece({self.row}, {self.col}, {'King' if self.king else 'Normal'})"
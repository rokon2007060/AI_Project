"""
Piece class for checkers game
"""
import pygame
from constants import SQUARE_SIZE, GREY, GOLD, CROWN

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
    
    def draw(self, win):
        """Draw the piece on the board"""
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.BORDER)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        
        if self.king:
            font = pygame.font.SysFont('arial', 40, bold=True)
            text = font.render(CROWN, True, GOLD)
            win.blit(text, (self.x - text.get_width() // 2, self.y - text.get_height() // 2))
    
    def move(self, row, col):
        """Move piece to new position"""
        self.row = row
        self.col = col
        self.calc_pos()
    
    def __repr__(self):
        return f"Piece({self.row}, {self.col}, {'King' if self.king else 'Normal'})"


"""
Constants for the Checkers game
"""

# ===== BOARD SIZE CONFIGURATION =====
# Change ROWS and COLS to adjust board size
# Standard checkers: 8x8
# You can try: 6x6 (smaller, faster), 10x10 (larger, more complex)
ROWS, COLS = 8, 8  # CHANGE THESE VALUES TO RESIZE BOARD

# ===== WINDOW SIZE CONFIGURATION =====
# Change BOARD_HEIGHT to resize the window to fit your screen
# Options: 500 (small), 600 (medium), 700 (large), 800 (extra large)
# If game goes outside screen, REDUCE this number!
BOARD_HEIGHT = 600  # CHANGE THIS TO FIT YOUR SCREEN! (try 500, 600, 700)

# Window dimensions (automatically calculated)
SQUARE_SIZE = BOARD_HEIGHT // COLS  # Each square size
INFO_PANEL_HEIGHT = 120  # Height of info panel at bottom
WIDTH = BOARD_HEIGHT  # Square window
HEIGHT = BOARD_HEIGHT + INFO_PANEL_HEIGHT  # Total window height

# Game rules
MAX_MOVES_WITHOUT_CAPTURE = 40  # Draw after N moves without capture
MAX_POSITION_REPEATS = 3  # Draw if same position repeats N times

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
LIGHT_BROWN = (240, 217, 181)
DARK_BROWN = (181, 136, 99)
GOLD = (255, 215, 0)
GREEN = (0, 200, 0)
LIGHT_BLUE = (173, 216, 230)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Piece colors
PLAYER1_COLOR = RED
PLAYER2_COLOR = WHITE

# Crown for kings
CROWN = "♔"

# Game modes
HUMAN_VS_HUMAN = "human_vs_human"
HUMAN_VS_AI = "human_vs_ai"
AI_VS_AI = "ai_vs_ai"


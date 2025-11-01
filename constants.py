"""
Constants for the Checkers game
"""

# ===== BOARD SIZE CONFIGURATION =====
ROWS, COLS = 8, 8  # Standard checkers board

# ===== WINDOW SIZE CONFIGURATION =====
BOARD_HEIGHT = 600  # Base board height

# Window dimensions (automatically calculated)
SQUARE_SIZE = BOARD_HEIGHT // COLS
INFO_PANEL_HEIGHT = 120
WIDTH = BOARD_HEIGHT
HEIGHT = BOARD_HEIGHT + INFO_PANEL_HEIGHT

# Game rules
MAX_MOVES_WITHOUT_CAPTURE = 50
MAX_POSITION_REPEATS = 5
STACKING_ENABLED = True
DRAW_RULES_ENABLED = True

# AI Configuration
AI_TYPE_ORIGINAL = "original"
AI_TYPE_FUZZY = "fuzzy" 
AI_TYPE_HEURISTIC = "heuristic"
AI_TYPE_MINIMAX_BACKTRACK = "minimax_backtrack"
AI_TYPE_MINIMAX_FUZZY = "minimax_fuzzy"

# Default AI types - Set to use the new agents by default
AI_PLAYER1_TYPE = AI_TYPE_MINIMAX_BACKTRACK  # Use Minimax+Backtrack by default
AI_PLAYER2_TYPE = AI_TYPE_MINIMAX_FUZZY      # Use Minimax+Fuzzy by default

# AI Search Parameters
AI_TIME_LIMIT = 5.0  # seconds per move
AI_DEPTH_MINIMAX = 4
AI_DEPTH_BACKTRACK = 3
AI_DEPTH_FUZZY = 4

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
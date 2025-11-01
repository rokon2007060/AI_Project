"""
Main file for Checkers Game
Supports: Human vs Human, Human vs AI, AI vs AI
"""
import pygame
import sys
import time
import constants
from constants import (PLAYER1_COLOR, PLAYER2_COLOR,
                       HUMAN_VS_HUMAN, HUMAN_VS_AI, AI_VS_AI, 
                       BLACK, WHITE, RED, BLUE, LIGHT_BLUE, GREEN, GOLD,
                       ROWS, YELLOW, ORANGE, AI_TYPE_ORIGINAL, AI_TYPE_FUZZY, 
                       AI_TYPE_HEURISTIC, AI_TYPE_MINIMAX_BACKTRACK, AI_TYPE_MINIMAX_FUZZY)
from game import Game
from ai_player import get_best_move
from ai_agents import MinimaxBacktrackAgent, MinimaxFuzzyAgent, FuzzyMinimaxAgent, HeuristicBacktrackAgent

FPS = 60
AI_VS_AI_DELAY = 1.0  # Delay in seconds between AI moves in AI vs AI mode

# Window will be created dynamically
WIN = None


def init_window():
    """Initialize or recreate the window with current constants"""
    global WIN
    WIN = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
    pygame.display.set_caption('Checkers Game')
    return WIN


def set_board_height(new_height):
    """Change board height and update all related constants"""
    constants.BOARD_HEIGHT = new_height
    constants.SQUARE_SIZE = constants.BOARD_HEIGHT // constants.COLS
    constants.WIDTH = constants.BOARD_HEIGHT
    constants.HEIGHT = constants.BOARD_HEIGHT + constants.INFO_PANEL_HEIGHT
    init_window()


def get_row_col_from_mouse(pos):
    """Convert mouse position to board row/col"""
    x, y = pos
    row = y // constants.SQUARE_SIZE
    col = x // constants.SQUARE_SIZE
    return row, col


def draw_size_selection(win):
    """Draw window size selection menu"""
    win.fill(BLACK)
    font_title = pygame.font.SysFont('arial', 50, bold=True)
    font_option = pygame.font.SysFont('arial', 35)
    font_small = pygame.font.SysFont('arial', 22)
    
    # Title
    title = font_title.render('SELECT WINDOW SIZE', True, GOLD)
    win.blit(title, (constants.WIDTH // 2 - title.get_width() // 2, 50))
    
    subtitle = font_small.render('Choose size that fits your screen', True, LIGHT_BLUE)
    win.blit(subtitle, (constants.WIDTH // 2 - subtitle.get_width() // 2, 110))
    
    # Size options
    options = [
        ("1. Small (500x620)", 500),
        ("2. Medium (600x720)", 600),
        ("3. Large (700x820)", 700),
        ("4. Extra Large (800x920)", 800)
    ]
    
    y_offset = 170
    for i, (option, size) in enumerate(options):
        # Highlight current size with checkmark
        if size == constants.BOARD_HEIGHT:
            color = GREEN
            display_option = f"✓ {option}"
        else:
            color = WHITE
            display_option = option
        
        text = font_option.render(display_option, True, color)
        win.blit(text, (constants.WIDTH // 2 - text.get_width() // 2, y_offset + i * 70))
    
    # Current size display
    current_text = font_small.render(f"Current: {constants.WIDTH}x{constants.HEIGHT}", True, YELLOW)
    win.blit(current_text, (constants.WIDTH // 2 - current_text.get_width() // 2, y_offset + 300))
    
    # Instructions
    instructions = [
        "Press 1, 2, 3, or 4 to change size",
        "Press ENTER or ESC to go back to menu"
    ]
    
    y_inst = y_offset + 340
    for i, inst in enumerate(instructions):
        text = font_small.render(inst, True, WHITE)
        win.blit(text, (constants.WIDTH // 2 - text.get_width() // 2, y_inst + i * 28))
    
    pygame.display.update()


def draw_board_size_selection(win):
    """Draw board size selection menu"""
    win.fill(BLACK)
    font_title = pygame.font.SysFont('arial', 50, bold=True)
    font_option = pygame.font.SysFont('arial', 35)
    font_small = pygame.font.SysFont('arial', 22)
    
    # Title
    title = font_title.render('SELECT BOARD SIZE', True, GOLD)
    win.blit(title, (constants.WIDTH // 2 - title.get_width() // 2, 50))
    
    subtitle = font_small.render('Number of rows and columns on the board', True, LIGHT_BLUE)
    win.blit(subtitle, (constants.WIDTH // 2 - subtitle.get_width() // 2, 110))
    
    # Size options
    options = [
        ("1. Tiny (6x6)", 6),
        ("2. Standard (8x8)", 8),
        ("3. Large (10x10)", 10),
        ("4. Extra Large (12x12)", 12)
    ]
    
    y_offset = 170
    for i, (option, size) in enumerate(options):
        # Highlight current size with checkmark
        if size == constants.ROWS:
            color = GREEN
            display_option = f"✓ {option}"
        else:
            color = WHITE
            display_option = option
        
        text = font_option.render(display_option, True, color)
        win.blit(text, (constants.WIDTH // 2 - text.get_width() // 2, y_offset + i * 70))
    
    # Current size display
    current_text = font_small.render(f"Current: {constants.ROWS}x{constants.COLS} board", True, YELLOW)
    win.blit(current_text, (constants.WIDTH // 2 - current_text.get_width() // 2, y_offset + 300))
    
    # Warning
    warning = font_small.render("Note: Larger boards may need more window space!", True, ORANGE)
    win.blit(warning, (constants.WIDTH // 2 - warning.get_width() // 2, y_offset + 330))
    
    # Instructions
    instructions = [
        "Press 1, 2, 3, or 4 to change board size",
        "Press ENTER or ESC to go back to menu"
    ]
    
    y_inst = y_offset + 370
    for i, inst in enumerate(instructions):
        text = font_small.render(inst, True, WHITE)
        win.blit(text, (constants.WIDTH // 2 - text.get_width() // 2, y_inst + i * 28))
    
    pygame.display.update()


def draw_ai_config(win):
    """Draw AI configuration menu"""
    win.fill(BLACK)
    font_title = pygame.font.SysFont('arial', 50, bold=True)
    font_option = pygame.font.SysFont('arial', 30)
    font_small = pygame.font.SysFont('arial', 22)
    
    # Title
    title = font_title.render('AI CONFIGURATION', True, GOLD)
    win.blit(title, (constants.WIDTH // 2 - title.get_width() // 2, 30))
    
    # AI type names
    ai_names = {
        AI_TYPE_ORIGINAL: "Original Minimax",
        AI_TYPE_MINIMAX_BACKTRACK: "Minimax + Backtrack (MRV/LCV)",
        AI_TYPE_MINIMAX_FUZZY: "Minimax + Fuzzy (Roulette)"
    }
    
    # Player 1 AI
    subtitle1 = font_small.render('RED Player AI (Player 1):', True, RED)
    win.blit(subtitle1, (constants.WIDTH // 2 - subtitle1.get_width() // 2, 100))
    
    options_p1 = [
        ("1. Original Minimax", AI_TYPE_ORIGINAL),
        ("2. Minimax + Backtracking", AI_TYPE_MINIMAX_BACKTRACK),
        ("3. Minimax + Fuzzy Logic", AI_TYPE_MINIMAX_FUZZY)
    ]
    
    y_offset = 135
    for i, (option, ai_type) in enumerate(options_p1):
        if constants.AI_PLAYER1_TYPE == ai_type:
            color = GREEN
            display_option = f"✓ {option}"
        else:
            color = WHITE
            display_option = option
        
        text = font_option.render(display_option, True, color)
        win.blit(text, (constants.WIDTH // 2 - text.get_width() // 2, y_offset + i * 50))
    
    # Player 2 AI
    subtitle2 = font_small.render('WHITE Player AI (Player 2):', True, WHITE)
    win.blit(subtitle2, (constants.WIDTH // 2 - subtitle2.get_width() // 2, 310))
    
    options_p2 = [
        ("4. Original Minimax", AI_TYPE_ORIGINAL),
        ("5. Minimax + Backtracking", AI_TYPE_MINIMAX_BACKTRACK),
        ("6. Minimax + Fuzzy Logic", AI_TYPE_MINIMAX_FUZZY)
    ]
    
    y_offset2 = 345
    for i, (option, ai_type) in enumerate(options_p2):
        if constants.AI_PLAYER2_TYPE == ai_type:
            color = GREEN
            display_option = f"✓ {option}"
        else:
            color = WHITE
            display_option = option
        
        text = font_option.render(display_option, True, color)
        win.blit(text, (constants.WIDTH // 2 - text.get_width() // 2, y_offset2 + i * 50))
    
    # Stacking toggle
    stacking_text = f"7. Stacking: {'ON' if constants.STACKING_ENABLED else 'OFF'}"
    stacking_color = GREEN if constants.STACKING_ENABLED else RED
    stacking_render = font_option.render(stacking_text, True, stacking_color)
    win.blit(stacking_render, (constants.WIDTH // 2 - stacking_render.get_width() // 2, 495))
    
    # Draw rules toggle
    draw_text = f"8. Draw Rules: {'ON' if constants.DRAW_RULES_ENABLED else 'OFF (Fight to Win!)'}"
    draw_color = GREEN if constants.DRAW_RULES_ENABLED else ORANGE
    draw_render = font_option.render(draw_text, True, draw_color)
    win.blit(draw_render, (constants.WIDTH // 2 - draw_render.get_width() // 2, 545))
    
    # Instructions
    instructions = [
        "Press 1-6 to select AI type, 7 to toggle stacking, 8 for draw rules",
        "Press ENTER or ESC to return to menu"
    ]
    
    y_inst = 600
    for i, inst in enumerate(instructions):
        text = font_small.render(inst, True, LIGHT_BLUE)
        win.blit(text, (constants.WIDTH // 2 - text.get_width() // 2, y_inst + i * 28))
    
    # AI descriptions at bottom
    desc_font = pygame.font.SysFont('arial', 16)
    descriptions = [
        "Original: Classic alpha-beta pruning minimax",
        "Minimax+Backtrack: Uses MRV/LCV heuristics with roulette wheel",
        "Minimax+Fuzzy: Uses fuzzy logic evaluation with roulette wheel"
    ]
    
    y_desc = 650
    for i, desc in enumerate(descriptions):
        text = desc_font.render(desc, True, LIGHT_BLUE)
        win.blit(text, (constants.WIDTH // 2 - text.get_width() // 2, y_desc + i * 20))
    
    pygame.display.update()


def draw_menu(win):
    """Draw the main menu"""
    win.fill(BLACK)
    font_title = pygame.font.SysFont('arial', 60, bold=True)
    font_option = pygame.font.SysFont('arial', 38)
    
    # Title
    title = font_title.render('CHECKERS GAME', True, GOLD)
    win.blit(title, (constants.WIDTH // 2 - title.get_width() // 2, 70))
    
    # Menu options
    options = [
        "1. Human vs Human",
        "2. Human vs AI",
        "3. AI vs AI",
        "4. Configure AI",
        "5. Change Board Size",
        "6. Change Window Size",
        "7. Quit"
    ]
    
    y_offset = 170
    for i, option in enumerate(options):
        color = WHITE
        text = font_option.render(option, True, color)
        win.blit(text, (constants.WIDTH // 2 - text.get_width() // 2, y_offset + i * 58))
    
    # Show current board size
    font_small = pygame.font.SysFont('arial', 18)
    board_info = f"Current Board: {constants.ROWS}x{constants.COLS}"
    board_text = font_small.render(board_info, True, LIGHT_BLUE)
    win.blit(board_text, (constants.WIDTH // 2 - board_text.get_width() // 2, 590))
    
    # Instructions
    instructions = [
        "Click on a piece to select it • Green circles show valid moves",
        "Yellow/Orange shows last move • Press 'R' to restart • 'M' for menu"
    ]
    
    y_inst = 620
    for i, inst in enumerate(instructions):
        text = font_small.render(inst, True, LIGHT_BLUE)
        win.blit(text, (constants.WIDTH // 2 - text.get_width() // 2, y_inst + i * 22))
    
    pygame.display.update()


def show_winner(win, winner_color, is_stalemate=False, draw_reason=None):
    """Display winner message"""
    overlay = pygame.Surface((constants.WIDTH, constants.HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    win.blit(overlay, (0, 0))
    
    font = pygame.font.SysFont('arial', 70, bold=True)
    font_small = pygame.font.SysFont('arial', 30)
    
    if draw_reason:
        # It's a draw
        winner_text = "DRAW!"
        color = YELLOW
        if draw_reason == "draw_no_capture":
            subtitle = font_small.render("Too many moves without capture", True, LIGHT_BLUE)
        elif draw_reason == "draw_repetition":
            subtitle = font_small.render("Same position repeated multiple times", True, LIGHT_BLUE)
        else:
            subtitle = font_small.render("Game ended in a draw", True, LIGHT_BLUE)
        win.blit(subtitle, (constants.WIDTH // 2 - subtitle.get_width() // 2, constants.HEIGHT // 2 - 30))
    elif is_stalemate:
        winner_text = "STALEMATE!"
        color = WHITE
        subtitle = font_small.render("No valid moves available", True, LIGHT_BLUE)
        win.blit(subtitle, (constants.WIDTH // 2 - subtitle.get_width() // 2, constants.HEIGHT // 2 - 30))
    else:
        winner_text = "RED WINS!" if winner_color == PLAYER1_COLOR else "WHITE WINS!"
        color = RED if winner_color == PLAYER1_COLOR else WHITE
    
    text = font.render(winner_text, True, color)
    win.blit(text, (constants.WIDTH // 2 - text.get_width() // 2, constants.HEIGHT // 2 - 100))
    
    font_small = pygame.font.SysFont('arial', 35)
    restart_text = font_small.render("Press 'R' to restart or 'M' for menu", True, WHITE)
    win.blit(restart_text, (constants.WIDTH // 2 - restart_text.get_width() // 2, constants.HEIGHT // 2 + 50))
    
    pygame.display.update()


def game_loop(mode):
    """Main game loop"""
    clock = pygame.time.Clock()
    game = Game(WIN)
    
    # AI settings
    ai_player1 = False  # Red player
    ai_player2 = False  # White player
    ai_depth = 4  # AI difficulty
    
    # Initialize AI agents
    ai_agent1 = None
    ai_agent2 = None
    
    # Setup AI agents based on game mode
    if mode == HUMAN_VS_AI:
        ai_player2 = True
        # Create AI agent for player 2 based on configuration
        if constants.AI_PLAYER2_TYPE == constants.AI_TYPE_MINIMAX_FUZZY:
            ai_agent2 = MinimaxFuzzyAgent(PLAYER2_COLOR, depth=constants.AI_DEPTH_FUZZY)
        elif constants.AI_PLAYER2_TYPE == constants.AI_TYPE_MINIMAX_BACKTRACK:
            ai_agent2 = MinimaxBacktrackAgent(PLAYER2_COLOR, depth=constants.AI_DEPTH_BACKTRACK)
        # else: use original AI (ai_agent2 remains None)

    elif mode == AI_VS_AI:
        ai_player1 = True
        ai_player2 = True
        # Create AI agents for both players based on configuration
        if constants.AI_PLAYER1_TYPE == constants.AI_TYPE_MINIMAX_FUZZY:
            ai_agent1 = MinimaxFuzzyAgent(PLAYER1_COLOR, depth=constants.AI_DEPTH_FUZZY)
        elif constants.AI_PLAYER1_TYPE == constants.AI_TYPE_MINIMAX_BACKTRACK:
            ai_agent1 = MinimaxBacktrackAgent(PLAYER1_COLOR, depth=constants.AI_DEPTH_BACKTRACK)
        
        if constants.AI_PLAYER2_TYPE == constants.AI_TYPE_MINIMAX_FUZZY:
            ai_agent2 = MinimaxFuzzyAgent(PLAYER2_COLOR, depth=constants.AI_DEPTH_FUZZY)
        elif constants.AI_PLAYER2_TYPE == constants.AI_TYPE_MINIMAX_BACKTRACK:
            ai_agent2 = MinimaxBacktrackAgent(PLAYER2_COLOR, depth=constants.AI_DEPTH_BACKTRACK)
    
    # Game state variables (for ALL modes)
    winner = None
    is_stalemate = False
    is_draw = False
    draw_reason = None
    ai_thinking = False
    last_ai_move_time = 0
    
    # Main game loop (for ALL modes)
    run = True
    while run:
        clock.tick(FPS)
        
        # Check for winner, stalemate, or draw
        if winner is None and not is_draw:
            # Check for regular winner first
            if game.winner() is not None:
                winner = game.winner()
                show_winner(WIN, winner, False)
            # Check for stalemate (no valid moves) - this ends the game
            elif not game.has_valid_moves(game.turn):
                is_stalemate = True
                # The player who can't move loses
                winner = PLAYER2_COLOR if game.turn == PLAYER1_COLOR else PLAYER1_COLOR
                show_winner(WIN, winner, True)
                print(f"STALEMATE DETECTED: {game.turn} has no valid moves. Winner: {winner}")
            # Check for draw conditions
            elif game.check_draw()[0]:
                is_draw, draw_reason = game.check_draw()
                show_winner(WIN, None, False, draw_reason)
        
        # AI turn logic
        current_player_is_ai = (game.turn == PLAYER1_COLOR and ai_player1) or \
                                (game.turn == PLAYER2_COLOR and ai_player2)
        
        if current_player_is_ai and winner is None and not is_draw and not ai_thinking:
            # Add delay for AI vs AI mode to make it watchable
            current_time = time.time()
            if mode == AI_VS_AI:
                if current_time - last_ai_move_time < AI_VS_AI_DELAY:
                    game.update()
                    continue
            
            ai_thinking = True
            
            # Determine which AI agent to use
            if game.turn == PLAYER1_COLOR:
                current_agent = ai_agent1
                agent_name = "Player 1 AI"
            else:
                current_agent = ai_agent2
                agent_name = "Player 2 AI"
            
            # Display AI type in caption
            if current_agent:
                ai_type_name = current_agent.__class__.__name__
                pygame.display.set_caption(f'Checkers - {agent_name} ({ai_type_name}) Thinking...')
            else:
                pygame.display.set_caption('Checkers Game - AI Thinking...')
            
            game.update()  # Show current state while AI thinks
            
            # Get AI move (use new agent if available, otherwise use original)
            if current_agent:
                new_board, move_info, was_capture = current_agent.get_move(game.get_board(), game)
                # Log performance stats
                if hasattr(current_agent, 'last_move_stats'):
                    stats = current_agent.last_move_stats
                    strategy = stats.get('strategy', 'unknown')
                    print(f"{agent_name} - Strategy: {strategy}, Nodes: {stats.get('nodes_expanded', 0)}, Time: {stats.get('time', 0):.2f}s")
            else:
                new_board, move_info, was_capture = get_best_move(game.get_board(), game.turn, ai_depth)
            
            # Check if AI has a valid move
            if new_board is not None:
                game.ai_move(new_board, move_info, was_capture)
            else:
                # AI has no valid moves - this should trigger stalemate
                print(f"{agent_name} has no valid moves!")
            
            last_ai_move_time = time.time()
            ai_thinking = False
            pygame.display.set_caption('Checkers Game')
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Restart game
                    game.reset()
                    winner = None
                    is_stalemate = False
                    is_draw = False
                    draw_reason = None
                    last_ai_move_time = 0
                
                if event.key == pygame.K_m:
                    # Return to menu
                    return
            
            if event.type == pygame.MOUSEBUTTONDOWN and not current_player_is_ai and winner is None and not is_draw:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                
                # Only process clicks on the board area (not info panel)
                if row < ROWS and pos[1] < constants.BOARD_HEIGHT:
                    game.select(row, col)
        
        # Always update display
        if winner is None and not is_draw:
            game.update()
        # If game ended, keep showing winner screen but still process events
        elif winner is not None or is_draw:
            # Keep the winner screen displayed but check for restart/menu keys
            pass


def board_size_selection_screen():
    """Show board size selection screen"""
    global WIN
    draw_board_size_selection(WIN)
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    constants.ROWS = 6
                    constants.COLS = 6
                    constants.SQUARE_SIZE = constants.BOARD_HEIGHT // constants.COLS
                    constants.WIDTH = constants.BOARD_HEIGHT
                    init_window()
                    draw_board_size_selection(WIN)
                
                elif event.key == pygame.K_2:
                    constants.ROWS = 8
                    constants.COLS = 8
                    constants.SQUARE_SIZE = constants.BOARD_HEIGHT // constants.COLS
                    constants.WIDTH = constants.BOARD_HEIGHT
                    init_window()
                    draw_board_size_selection(WIN)
                
                elif event.key == pygame.K_3:
                    constants.ROWS = 10
                    constants.COLS = 10
                    constants.SQUARE_SIZE = constants.BOARD_HEIGHT // constants.COLS
                    constants.WIDTH = constants.BOARD_HEIGHT
                    init_window()
                    draw_board_size_selection(WIN)
                
                elif event.key == pygame.K_4:
                    constants.ROWS = 12
                    constants.COLS = 12
                    constants.SQUARE_SIZE = constants.BOARD_HEIGHT // constants.COLS
                    constants.WIDTH = constants.BOARD_HEIGHT
                    init_window()
                    draw_board_size_selection(WIN)
                
                elif event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    waiting = False
                    return True
            
            # Add mouse click support
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                y_offset = 170
                option_height = 70
                
                # Check if clicked on any size option
                if y_offset <= y < y_offset + option_height:
                    constants.ROWS = 6
                    constants.COLS = 6
                    constants.SQUARE_SIZE = constants.BOARD_HEIGHT // constants.COLS
                    constants.WIDTH = constants.BOARD_HEIGHT
                    init_window()
                    draw_board_size_selection(WIN)
                elif y_offset + option_height <= y < y_offset + 2*option_height:
                    constants.ROWS = 8
                    constants.COLS = 8
                    constants.SQUARE_SIZE = constants.BOARD_HEIGHT // constants.COLS
                    constants.WIDTH = constants.BOARD_HEIGHT
                    init_window()
                    draw_board_size_selection(WIN)
                elif y_offset + 2*option_height <= y < y_offset + 3*option_height:
                    constants.ROWS = 10
                    constants.COLS = 10
                    constants.SQUARE_SIZE = constants.BOARD_HEIGHT // constants.COLS
                    constants.WIDTH = constants.BOARD_HEIGHT
                    init_window()
                    draw_board_size_selection(WIN)
                elif y_offset + 3*option_height <= y < y_offset + 4*option_height:
                    constants.ROWS = 12
                    constants.COLS = 12
                    constants.SQUARE_SIZE = constants.BOARD_HEIGHT // constants.COLS
                    constants.WIDTH = constants.BOARD_HEIGHT
                    init_window()
                    draw_board_size_selection(WIN)
    
    return True


def size_selection_screen():
    """Show window size selection screen"""
    global WIN
    draw_size_selection(WIN)
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    set_board_height(500)
                    draw_size_selection(WIN)
                
                elif event.key == pygame.K_2:
                    set_board_height(600)
                    draw_size_selection(WIN)
                
                elif event.key == pygame.K_3:
                    set_board_height(700)
                    draw_size_selection(WIN)
                
                elif event.key == pygame.K_4:
                    set_board_height(800)
                    draw_size_selection(WIN)
                
                elif event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    waiting = False
                    return True
            
            # Add mouse click support for size options
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                y_offset = 170
                option_height = 70
                
                # Check if clicked on any size option
                if y_offset <= y < y_offset + option_height:
                    set_board_height(500)
                    draw_size_selection(WIN)
                elif y_offset + option_height <= y < y_offset + 2*option_height:
                    set_board_height(600)
                    draw_size_selection(WIN)
                elif y_offset + 2*option_height <= y < y_offset + 3*option_height:
                    set_board_height(700)
                    draw_size_selection(WIN)
                elif y_offset + 3*option_height <= y < y_offset + 4*option_height:
                    set_board_height(800)
                    draw_size_selection(WIN)
    
    return True


def ai_config_screen():
    """Show AI configuration screen"""
    global WIN
    draw_ai_config(WIN)
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                # Player 1 AI selection
                if event.key == pygame.K_1:
                    constants.AI_PLAYER1_TYPE = AI_TYPE_ORIGINAL
                    draw_ai_config(WIN)
                elif event.key == pygame.K_2:
                    constants.AI_PLAYER1_TYPE = AI_TYPE_MINIMAX_BACKTRACK
                    draw_ai_config(WIN)
                elif event.key == pygame.K_3:
                    constants.AI_PLAYER1_TYPE = AI_TYPE_MINIMAX_FUZZY
                    draw_ai_config(WIN)
                
                # Player 2 AI selection
                elif event.key == pygame.K_4:
                    constants.AI_PLAYER2_TYPE = AI_TYPE_ORIGINAL
                    draw_ai_config(WIN)
                elif event.key == pygame.K_5:
                    constants.AI_PLAYER2_TYPE = AI_TYPE_MINIMAX_BACKTRACK
                    draw_ai_config(WIN)
                elif event.key == pygame.K_6:
                    constants.AI_PLAYER2_TYPE = AI_TYPE_MINIMAX_FUZZY
                    draw_ai_config(WIN)
                
                # Stacking toggle
                elif event.key == pygame.K_7:
                    constants.STACKING_ENABLED = not constants.STACKING_ENABLED
                    draw_ai_config(WIN)
                
                # Draw rules toggle
                elif event.key == pygame.K_8:
                    constants.DRAW_RULES_ENABLED = not constants.DRAW_RULES_ENABLED
                    draw_ai_config(WIN)
                
                # Return to menu
                elif event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    waiting = False
                    return True
    
    return True


def main():
    """Main function - shows menu and starts game"""
    global WIN
    pygame.init()
    WIN = init_window()
    
    # Show size selection on first run
    size_selection_screen()
    
    while True:
        draw_menu(WIN)
        
        # Wait for menu selection
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        waiting = False
                        game_loop(HUMAN_VS_HUMAN)
                    
                    elif event.key == pygame.K_2:
                        waiting = False
                        game_loop(HUMAN_VS_AI)
                    
                    elif event.key == pygame.K_3:
                        waiting = False
                        game_loop(AI_VS_AI)
                    
                    elif event.key == pygame.K_4:
                        ai_config_screen()
                        waiting = False
                    
                    elif event.key == pygame.K_5:
                        board_size_selection_screen()
                        waiting = False
                    
                    elif event.key == pygame.K_6:
                        size_selection_screen()
                        waiting = False
                    
                    elif event.key == pygame.K_7:
                        pygame.quit()
                        sys.exit()
                
                # Mouse click on menu options
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    x, y = pos
                    
                    # Check which option was clicked
                    y_offset = 170
                    option_height = 58
                    
                    if y_offset <= y < y_offset + option_height:
                        waiting = False
                        game_loop(HUMAN_VS_HUMAN)
                    elif y_offset + option_height <= y < y_offset + 2*option_height:
                        waiting = False
                        game_loop(HUMAN_VS_AI)
                    elif y_offset + 2*option_height <= y < y_offset + 3*option_height:
                        waiting = False
                        game_loop(AI_VS_AI)
                    elif y_offset + 3*option_height <= y < y_offset + 4*option_height:
                        ai_config_screen()
                        waiting = False
                    elif y_offset + 4*option_height <= y < y_offset + 5*option_height:
                        board_size_selection_screen()
                        waiting = False
                    elif y_offset + 5*option_height <= y < y_offset + 6*option_height:
                        size_selection_screen()
                        waiting = False
                    elif y_offset + 6*option_height <= y < y_offset + 7*option_height:
                        pygame.quit()
                        sys.exit()


if __name__ == '__main__':
    main()
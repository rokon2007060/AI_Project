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
                       ROWS, YELLOW)
from game import Game
from ai_player import get_best_move

FPS = 60
AI_VS_AI_DELAY = 1.5  # Delay in seconds between AI moves in AI vs AI mode

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
    
    # Instructions - more clear
    instructions = [
        "Press 1, 2, 3, or 4 to change size",
        "Press ENTER or ESC to go back to menu"
    ]
    
    y_inst = y_offset + 340
    for i, inst in enumerate(instructions):
        text = font_small.render(inst, True, WHITE)
        win.blit(text, (constants.WIDTH // 2 - text.get_width() // 2, y_inst + i * 28))
    
    pygame.display.update()


def draw_menu(win):
    """Draw the main menu"""
    win.fill(BLACK)
    font_title = pygame.font.SysFont('arial', 60, bold=True)
    font_option = pygame.font.SysFont('arial', 40)
    
    # Title
    title = font_title.render('CHECKERS GAME', True, GOLD)
    win.blit(title, (constants.WIDTH // 2 - title.get_width() // 2, 80))
    
    # Menu options
    options = [
        "1. Human vs Human",
        "2. Human vs AI",
        "3. AI vs AI",
        "4. Change Window Size",
        "5. Quit"
    ]
    
    y_offset = 220
    for i, option in enumerate(options):
        color = WHITE
        text = font_option.render(option, True, color)
        win.blit(text, (constants.WIDTH // 2 - text.get_width() // 2, y_offset + i * 70))
    
    # Instructions
    font_small = pygame.font.SysFont('arial', 23)
    instructions = [
        "Click on a piece to select it",
        "Green circles show valid moves",
        "Yellow/Orange shows last move",
        "Press 'R' to restart • 'M' for menu"
    ]
    
    y_inst = 580
    for i, inst in enumerate(instructions):
        text = font_small.render(inst, True, LIGHT_BLUE)
        win.blit(text, (constants.WIDTH // 2 - text.get_width() // 2, y_inst + i * 30))
    
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
            subtitle = font_small.render("Same position repeated 3 times", True, LIGHT_BLUE)
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
    ai_depth = 3  # AI difficulty (higher = smarter but slower)
    
    if mode == HUMAN_VS_AI:
        ai_player2 = True
    elif mode == AI_VS_AI:
        ai_player1 = True
        ai_player2 = True
        ai_depth = 3  # Can adjust for different difficulty
    
    winner = None
    is_stalemate = False
    is_draw = False
    draw_reason = None
    ai_thinking = False
    last_ai_move_time = 0
    
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
            pygame.display.set_caption('Checkers Game - AI Thinking...')
            game.update()  # Show current state while AI thinks
            
            # Get AI move
            new_board, move_info, was_capture = get_best_move(game.get_board(), game.turn, ai_depth)
            
            # Check if AI has a valid move
            if new_board is not None:
                game.ai_move(new_board, move_info, was_capture)
            
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
        # If game ended, keep showing winner screen
        elif winner is not None or is_draw:
            pass  # Winner screen is already showing, don't redraw board
    
    pygame.quit()
    sys.exit()


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
                    # Return to main menu
                    waiting = False
                    return True  # Signal successful return
            
            # Add mouse click support for size options
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                y_offset = 170
                option_height = 70
                
                # Check if clicked on any size option
                if y_offset <= y < y_offset + option_height:  # Option 1
                    set_board_height(500)
                    draw_size_selection(WIN)
                elif y_offset + option_height <= y < y_offset + 2*option_height:  # Option 2
                    set_board_height(600)
                    draw_size_selection(WIN)
                elif y_offset + 2*option_height <= y < y_offset + 3*option_height:  # Option 3
                    set_board_height(700)
                    draw_size_selection(WIN)
                elif y_offset + 3*option_height <= y < y_offset + 4*option_height:  # Option 4
                    set_board_height(800)
                    draw_size_selection(WIN)
    
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
                        size_selection_screen()
                        waiting = False
                    
                    elif event.key == pygame.K_5:
                        pygame.quit()
                        sys.exit()
                
                # Mouse click on menu options
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    x, y = pos
                    
                    # Check which option was clicked (adjusted for 5 options)
                    y_offset = 220
                    option_height = 70
                    
                    if y_offset <= y < y_offset + option_height:  # Human vs Human
                        waiting = False
                        game_loop(HUMAN_VS_HUMAN)
                    elif y_offset + option_height <= y < y_offset + 2*option_height:  # Human vs AI
                        waiting = False
                        game_loop(HUMAN_VS_AI)
                    elif y_offset + 2*option_height <= y < y_offset + 3*option_height:  # AI vs AI
                        waiting = False
                        game_loop(AI_VS_AI)
                    elif y_offset + 3*option_height <= y < y_offset + 4*option_height:  # Change Size
                        size_selection_screen()
                        waiting = False
                    elif y_offset + 4*option_height <= y < y_offset + 5*option_height:  # Quit
                        pygame.quit()
                        sys.exit()


if __name__ == '__main__':
    main()


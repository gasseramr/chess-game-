import pygame
import chess
import random
import time
import math

# Initialize Pygame
pygame.init()

# Constants
BOARD_SIZE = 600
SQUARE_SIZE = BOARD_SIZE // 8
PANEL_WIDTH = 300
WINDOW_WIDTH = BOARD_SIZE + PANEL_WIDTH
WINDOW_HEIGHT = BOARD_SIZE
WHITE = (240, 217, 181)
BLACK = (181, 136, 99)
WHITE_HIGHLIGHT = (255, 255, 0, 128)  # Yellow for selected
BLACK_HIGHLIGHT = (255, 165, 0, 128)   # Orange for moves
MOVE_HIGHLIGHT = (0, 255, 0, 128)      # Green for valid moves
CHECK_HIGHLIGHT = (255, 0, 0, 128)     # Red for check
PANEL_BG = (45, 45, 45)                # Dark gray panel
TEXT_COLOR = (255, 255, 255)           # White text
BUTTON_COLOR = (70, 70, 70)            # Button background
BUTTON_HOVER = (90, 90, 90)            # Button hover color

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Enhanced Chess Game")
FONT_LARGE = pygame.font.Font(pygame.font.match_font("arial"), 24)
FONT_MEDIUM = pygame.font.Font(pygame.font.match_font("arial"), 18)
FONT_SMALL = pygame.font.Font(pygame.font.match_font("arial"), 14)

# Load piece images
PIECES = {}
for piece, path in [
    ("K", "assets/white/wk.png"),
    ("Q", "assets/white/wq.png"),
    ("R", "assets/white/wr.png"),
    ("B", "assets/white/wb.png"),
    ("N", "assets/white/wn.png"),
    ("P", "assets/white/wp.png"),
    ("k", "assets/black/bk.png"),
    ("q", "assets/black/bq.png"),
    ("r", "assets/black/br.png"),
    ("b", "assets/black/bb.png"),
    ("n", "assets/black/bn.png"),
    ("p", "assets/black/bp.png"),
]:
    PIECES[piece] = pygame.transform.scale(
        pygame.image.load(path), (SQUARE_SIZE, SQUARE_SIZE)
    )

class Button:
    def __init__(self, x, y, width, height, text, font=FONT_MEDIUM):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = BUTTON_COLOR
        self.hover = False
        
    def draw(self, surface):
        color = BUTTON_HOVER if self.hover else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, TEXT_COLOR, self.rect, 2)
        
        text_surface = self.font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hover:
                return True
        return False

class GameState:
    def __init__(self):
        self.board = chess.Board()
        self.selected_square = None
        self.move_history = []  # Store (move, san_move) tuples
        self.game_over = False
        self.winner = None
        self.difficulty = "medium"
        self.current_player = "White"
        self.last_move = None
        self.animation_time = 0
        self.animation_duration = 0.3  # seconds
        self.ai_last_moves = []  # Track AI's last few moves to prevent repetition

def draw_gradient_background(surface, color1, color2):
    """Draw a gradient background"""
    for y in range(surface.get_height()):
        ratio = y / surface.get_height()
        color = [
            int(color1[i] * (1 - ratio) + color2[i] * ratio)
            for i in range(3)
        ]
        pygame.draw.line(surface, color, (0, y), (surface.get_width(), y))

def draw_board():
    """Draw the chessboard with enhanced styling"""
    # Draw gradient background for the board area
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            # Add subtle gradient effect
            if (row + col) % 2 == 0:
                color = (min(255, color[0] + 10), min(255, color[1] + 10), min(255, color[2] + 10))
            pygame.draw.rect(
                WINDOW,
                color,
                (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
            )
            # Add border
            pygame.draw.rect(
                WINDOW,
                (100, 100, 100),
                (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                1
            )

def draw_pieces(board, game_state):
    """Draw pieces with animation support"""
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            col = square % 8
            row = square // 8
            
            # Animation for last move
            offset_x, offset_y = 0, 0
            if game_state.last_move and square in [game_state.last_move.from_square, game_state.last_move.to_square]:
                if game_state.animation_time < game_state.animation_duration:
                    progress = game_state.animation_time / game_state.animation_duration
                    # Simple bounce animation
                    offset_y = -5 * math.sin(progress * math.pi)
            
            x = col * SQUARE_SIZE + offset_x
            y = row * SQUARE_SIZE + offset_y
            WINDOW.blit(PIECES[str(piece)], (x, y))

def highlight_squares(board, game_state):
    """Enhanced highlighting with multiple colors"""
    # Highlight selected piece
    if game_state.selected_square is not None:
        col = game_state.selected_square % 8
        row = game_state.selected_square // 8
        highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(highlight_surface, WHITE_HIGHLIGHT, (0, 0, SQUARE_SIZE, SQUARE_SIZE))
        WINDOW.blit(highlight_surface, (col * SQUARE_SIZE, row * SQUARE_SIZE))
        
        # Highlight possible moves
        for move in board.legal_moves:
            if move.from_square == game_state.selected_square:
                to_col = move.to_square % 8
                to_row = move.to_square // 8
                
                # Different color for captures
                target_piece = board.piece_at(move.to_square)
                if target_piece:
                    highlight_color = (255, 0, 0, 128)  # Red for captures
                else:
                    highlight_color = MOVE_HIGHLIGHT
                
                highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                pygame.draw.rect(highlight_surface, highlight_color, (0, 0, SQUARE_SIZE, SQUARE_SIZE))
                WINDOW.blit(highlight_surface, (to_col * SQUARE_SIZE, to_row * SQUARE_SIZE))
    
    # Highlight king in check
    if board.is_check():
        king_square = board.king(board.turn)
        if king_square is not None:
            col = king_square % 8
            row = king_square // 8
            highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(highlight_surface, CHECK_HIGHLIGHT, (0, 0, SQUARE_SIZE, SQUARE_SIZE))
            WINDOW.blit(highlight_surface, (col * SQUARE_SIZE, row * SQUARE_SIZE))

def draw_panel(game_state):
    """Draw the side panel with game information"""
    panel_x = BOARD_SIZE
    
    # Draw panel background
    pygame.draw.rect(WINDOW, PANEL_BG, (panel_x, 0, PANEL_WIDTH, WINDOW_HEIGHT))
    
    # Draw gradient overlay
    draw_gradient_background(WINDOW.subsurface((panel_x, 0, PANEL_WIDTH, WINDOW_HEIGHT)), 
                           PANEL_BG, (60, 60, 60))
    
    y_offset = 20
    
    # Game title
    title_text = FONT_LARGE.render("Chess Game", True, TEXT_COLOR)
    WINDOW.blit(title_text, (panel_x + 10, y_offset))
    y_offset += 50
    
    # Current player
    player_text = FONT_MEDIUM.render(f"Current Player: {game_state.current_player}", True, TEXT_COLOR)
    WINDOW.blit(player_text, (panel_x + 10, y_offset))
    y_offset += 40
    
    # Game status
    if game_state.game_over:
        status_text = FONT_MEDIUM.render(f"Game Over - {game_state.winner} wins!", True, (255, 255, 0))
    elif game_state.board.is_check():
        status_text = FONT_MEDIUM.render("Check!", True, (255, 0, 0))
    elif game_state.board.is_checkmate():
        status_text = FONT_MEDIUM.render("Checkmate!", True, (255, 0, 0))
    elif game_state.board.is_stalemate():
        status_text = FONT_MEDIUM.render("Stalemate!", True, (255, 165, 0))
    else:
        status_text = FONT_MEDIUM.render("Game in progress", True, (0, 255, 0))
    
    WINDOW.blit(status_text, (panel_x + 10, y_offset))
    y_offset += 40
    
    # Difficulty
    diff_text = FONT_MEDIUM.render(f"Difficulty: {game_state.difficulty.title()}", True, TEXT_COLOR)
    WINDOW.blit(diff_text, (panel_x + 10, y_offset))
    y_offset += 60
    
    # Move history - limit to avoid overlapping with buttons
    history_area_height = WINDOW_HEIGHT - 250  # Leave space for buttons
    max_moves = (history_area_height - y_offset) // 20  # 20 pixels per move
    
    for i, (move_obj, san_move) in enumerate(game_state.move_history[-max_moves:]):
        move_text = FONT_SMALL.render(f"{len(game_state.move_history) - max_moves + i + 1}. {san_move}", True, TEXT_COLOR)
        WINDOW.blit(move_text, (panel_x + 10, y_offset))
        y_offset += 20

def create_buttons():
    """Create game control buttons"""
    buttons = []
    button_y = WINDOW_HEIGHT - 200
    
    buttons.append(Button(BOARD_SIZE + 20, button_y, 120, 40, "New Game"))
    buttons.append(Button(BOARD_SIZE + 150, button_y, 120, 40, "Reset"))
    button_y += 50
    buttons.append(Button(BOARD_SIZE + 20, button_y, 120, 40, "Undo"))
    buttons.append(Button(BOARD_SIZE + 150, button_y, 120, 40, "Settings"))
    
    return buttons

def handle_user_move(board, mouse_pos, selected_square):
    """Enhanced move handling with better feedback"""
    if mouse_pos[0] >= BOARD_SIZE:  # Clicked on panel
        return False, selected_square, None, None
        
    col = mouse_pos[0] // SQUARE_SIZE
    row = mouse_pos[1] // SQUARE_SIZE
    square = row * 8 + col
    
    if selected_square is not None:
        move = chess.Move(selected_square, square)
        
        # Handle pawn promotion
        piece = board.piece_at(selected_square)
        if piece and piece.piece_type == chess.PAWN:
            if (piece.color and chess.square_rank(selected_square) == 6) or (
                not piece.color and chess.square_rank(selected_square) == 1
            ):
                promotion_piece = prompt_for_promotion(piece.color)
                if promotion_piece:
                    move.promotion = promotion_piece.piece_type
        
        if move in board.legal_moves:
            # Get SAN notation before pushing the move
            san_move = board.san(move)
            board.push(move)
            return True, None, move, san_move
        else:
            if selected_square == square:
                return False, None, None, None
            elif board.piece_at(square) and board.piece_at(square).color == board.turn:
                return False, square, None, None
            return False, selected_square, None, None
    
    if board.piece_at(square) and board.piece_at(square).color == board.turn:
        return False, square, None, None
    
    return False, None, None, None

def prompt_for_promotion(color):
    """Enhanced promotion dialog"""
    # Create overlay surface
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    WINDOW.blit(overlay, (0, 0))
    
    # Draw promotion dialog
    dialog_rect = pygame.Rect(WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2 - 100, 300, 200)
    pygame.draw.rect(WINDOW, (50, 50, 50), dialog_rect)
    pygame.draw.rect(WINDOW, TEXT_COLOR, dialog_rect, 3)
    
    title_text = FONT_LARGE.render("Promote Pawn", True, TEXT_COLOR)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 60))
    WINDOW.blit(title_text, title_rect)
    
    options = [
        ("Q", "Queen"),
        ("R", "Rook"),
        ("B", "Bishop"),
        ("N", "Knight")
    ]
    
    for i, (key, name) in enumerate(options):
        text = FONT_MEDIUM.render(f"Press '{key}' for {name}", True, TEXT_COLOR)
        text_rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 20 + i*30))
        WINDOW.blit(text, text_rect)
    
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return chess.Piece(chess.QUEEN, color)
                elif event.key == pygame.K_r:
                    return chess.Piece(chess.ROOK, color)
                elif event.key == pygame.K_b:
                    return chess.Piece(chess.BISHOP, color)
                elif event.key == pygame.K_n:
                    return chess.Piece(chess.KNIGHT, color)

def welcome_menu():
    """Enhanced welcome menu"""
    WINDOW.fill((30, 30, 30))
    draw_gradient_background(WINDOW, (30, 30, 30), (60, 60, 60))
    
    # Draw chess pieces as decoration
    for i in range(4):
        piece_key = list(PIECES.keys())[i]
        WINDOW.blit(PIECES[piece_key], (50 + i*100, 50))
        WINDOW.blit(PIECES[piece_key.lower()], (50 + i*100, WINDOW_HEIGHT - 100))
    
    title_text = FONT_LARGE.render("Enhanced Chess Game", True, TEXT_COLOR)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//3))
    WINDOW.blit(title_text, title_rect)
    
    subtitle_text = FONT_MEDIUM.render("A Python-based chess game with AI", True, (200, 200, 200))
    subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//3 + 40))
    WINDOW.blit(subtitle_text, subtitle_rect)
    
    start_text = FONT_MEDIUM.render("Press 'S' to Start", True, (0, 255, 0))
    start_rect = start_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
    WINDOW.blit(start_text, start_rect)
    
    quit_text = FONT_MEDIUM.render("Press 'Q' to Quit", True, (255, 0, 0))
    quit_rect = quit_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 40))
    WINDOW.blit(quit_text, quit_rect)
    
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()

def level_selection_menu():
    """Enhanced difficulty selection menu"""
    WINDOW.fill((30, 30, 30))
    draw_gradient_background(WINDOW, (30, 30, 30), (60, 60, 60))
    
    title_text = FONT_LARGE.render("Select Difficulty Level", True, TEXT_COLOR)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//4))
    WINDOW.blit(title_text, title_rect)
    
    difficulties = [
        ("1", "Easy", "Random moves"),
        ("2", "Medium", "Basic strategy"),
        ("3", "Hard", "Advanced AI")
    ]
    
    for i, (key, name, desc) in enumerate(difficulties):
        y_pos = WINDOW_HEIGHT//2 - 50 + i*60
        key_text = FONT_LARGE.render(f"{key}. {name}", True, (0, 255, 0))
        key_rect = key_text.get_rect(center=(WINDOW_WIDTH//2, y_pos))
        WINDOW.blit(key_text, key_rect)
        
        desc_text = FONT_SMALL.render(desc, True, (200, 200, 200))
        desc_rect = desc_text.get_rect(center=(WINDOW_WIDTH//2, y_pos + 25))
        WINDOW.blit(desc_text, desc_rect)
    
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "easy"
                elif event.key == pygame.K_2:
                    return "medium"
                elif event.key == pygame.K_3:
                    return "hard"

def ai_move_mcts(board, time_limit=5):
    """Enhanced AI move with better time management"""
    start_time = time.time()
    move_scores = {move: 0 for move in board.legal_moves}
    move_counts = {move: 0 for move in board.legal_moves}
    
    def simulate(board_copy):
        while not board_copy.is_game_over():
            move = random.choice(list(board_copy.legal_moves))
            board_copy.push(move)
    
    while time.time() - start_time < time_limit:
        for move in move_scores.keys():
            board_copy = board.copy()
            board_copy.push(move)
            simulate(board_copy)
            
            if board_copy.result() == "1-0":
                move_scores[move] += 1
            elif board_copy.result() == "0-1":
                move_scores[move] -= 1
            move_counts[move] += 1
    
    best_move = max(
        move_scores,
        key=lambda m: (
            move_scores[m] / move_counts[m] if move_counts[m] > 0 else float("-inf")
        ),
    )
    return best_move

def evaluate_board(board):
    """Enhanced board evaluation with aggressive attacking style"""
    values = {
        "P": 1, "N": 3, "B": 3, "R": 5, "Q": 9, "K": 0,
        "p": -1, "n": -3, "b": -3, "r": -5, "q": -9, "k": 0,
    }
    
    # Aggressive piece-square tables for attacking play
    pawn_table = [
        0,  0,  0,  0,  0,  0,  0,  0,
        50, 50, 50, 50, 50, 50, 50, 50,
        20, 20, 30, 40, 40, 30, 20, 20,  # More aggressive pawn advancement
        15, 15, 25, 35, 35, 25, 15, 15,
        10, 10, 20, 30, 30, 20, 10, 10,
        5,  5, 15, 25, 25, 15,  5,  5,
        0,  0, 10, 20, 20, 10,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0
    ]
    
    knight_table = [
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  5,  5,  0,-20,-40,  # More aggressive knight positioning
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 20, 25, 25, 20,  0,-30,
        -30,  5, 20, 25, 25, 20,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50
    ]
    
    bishop_table = [
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10,  5,  0,  0,  0,  0,  5,-10,  # More aggressive bishop positioning
        -10, 10, 10, 10, 10, 10, 10,-10,
        -10,  0, 10, 10, 10, 10,  0,-10,
        -10,  5,  5, 10, 10,  5,  5,-10,
        -10,  0,  5, 10, 10,  5,  0,-10,
        -10,  5,  0,  0,  0,  0,  5,-10,
        -20,-10,-10,-10,-10,-10,-10,-20
    ]
    
    rook_table = [
        0,  0,  0,  0,  0,  0,  0,  0,
        5, 10, 10, 10, 10, 10, 10,  5,
        0,  0,  0,  0,  0,  0,  0,  0,  # Rooks prefer open files
        0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  5,  5,  0,  0,  0
    ]
    
    queen_table = [
        -20,-10,-10, -5, -5,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5,  5,  5,  5,  0,-10,
        -5,  0,  5,  5,  5,  5,  0, -5,
        0,  0,  5,  5,  5,  5,  0, -5,  # Queen more active in center
        -10,  5,  5,  5,  5,  5,  0,-10,
        -10,  0,  5,  0,  0,  0,  0,-10,
        -20,-10,-10, -5, -5,-10,-10,-20
    ]
    
    king_table = [
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -20,-30,-30,-40,-40,-30,-30,-20,
        -10,-20,-20,-20,-20,-20,-20,-10,
        20, 20,  0,  0,  0,  0, 20, 20,
        20, 30, 10,  0,  0, 10, 30, 20
    ]
    
    eval = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            # Basic piece value
            eval += values[str(piece)]
            
            # Positional bonus
            col = square % 8
            row = square // 8
            if piece.color:  # White pieces
                pos = square
            else:  # Black pieces
                pos = 63 - square  # Mirror for black
                
            if piece.piece_type == chess.PAWN:
                eval += pawn_table[pos] * 0.15  # Increased pawn value
            elif piece.piece_type == chess.KNIGHT:
                eval += knight_table[pos] * 0.15
            elif piece.piece_type == chess.BISHOP:
                eval += bishop_table[pos] * 0.15
            elif piece.piece_type == chess.ROOK:
                eval += rook_table[pos] * 0.15
            elif piece.piece_type == chess.QUEEN:
                eval += queen_table[pos] * 0.15
            elif piece.piece_type == chess.KING:
                eval += king_table[pos] * 0.15
    
    # Aggressive bonuses for attacking play
    # Bonus for controlling center
    center_squares = [chess.E4, chess.E5, chess.D4, chess.D5]
    for square in center_squares:
        piece = board.piece_at(square)
        if piece:
            eval += 0.4 if piece.color else -0.4  # Increased center control bonus
    
    # Bonus for attacking squares near enemy king
    enemy_king = board.king(not board.turn)
    if enemy_king is not None:
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.color == board.turn:
                # Calculate distance to enemy king
                king_distance = abs(square % 8 - enemy_king % 8) + abs(square // 8 - enemy_king // 8)
                if king_distance <= 4:  # Pieces within 4 squares of enemy king
                    eval += 0.3  # Aggressive bonus for attacking pieces
    
    # Bonus for developed pieces (knights and bishops moved from starting position)
    for square in [chess.B1, chess.G1, chess.B8, chess.G8]:  # Knight starting squares
        piece = board.piece_at(square)
        if piece and piece.piece_type == chess.KNIGHT:
            eval += -0.5 if piece.color else 0.5  # Increased penalty for undeveloped knights
    
    for square in [chess.C1, chess.F1, chess.C8, chess.F8]:  # Bishop starting squares
        piece = board.piece_at(square)
        if piece and piece.piece_type == chess.BISHOP:
            eval += -0.5 if piece.color else 0.5  # Increased penalty for undeveloped bishops
    
    # Bonus for attacking moves and piece activity
    if board.is_check():
        eval += 0.5 if board.turn else -0.5  # Bonus for being in check (attacking)
    
    return eval

def get_opening_move(board):
    """Simple opening book for better early game play"""
    # Common opening moves
    opening_moves = {
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1": ["e4", "d4", "c4", "Nf3"],  # Starting position
        "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1": ["e5", "e6", "c5", "Nf6"],  # After e4
        "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1": ["d5", "Nf6", "e6", "c5"],  # After d4
        "rnbqkbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR b KQkq - 0 1": ["e5", "d5", "Nf6", "c5"],  # After c4
    }
    
    fen = board.fen()
    if fen in opening_moves:
        moves = opening_moves[fen]
        for move_san in moves:
            try:
                move = board.parse_san(move_san)
                if move in board.legal_moves:
                    return move
            except:
                continue
    return None

def get_smart_ai_move(board, game_state):
    """Enhanced AI move selection with aggressive attacking style"""
    legal_moves = list(board.legal_moves)
    
    # Remove recently played moves to prevent repetition
    recent_moves = game_state.ai_last_moves[-4:]  # Last 4 moves
    filtered_moves = [move for move in legal_moves if move not in recent_moves]
    
    # If we have filtered moves, use them; otherwise use all legal moves
    if filtered_moves:
        legal_moves = filtered_moves
    
    # Score all moves
    move_scores = []
    for move in legal_moves:
        score = 0
        
        # Basic evaluation
        board.push(move)
        score += evaluate_board(board)
        board.pop()
        
        # Aggressive bonuses for attacking play
        
        # Bonus for captures (increased for aggressive play)
        if board.piece_at(move.to_square):
            score += 1.0  # Increased capture bonus
        
        # Bonus for center control (increased)
        if move.to_square in [chess.E4, chess.E5, chess.D4, chess.D5]:
            score += 0.6  # Increased center control bonus
        
        # Bonus for developing pieces early (increased)
        if len(game_state.move_history) < 10:
            piece = board.piece_at(move.from_square)
            if piece and piece.piece_type in [chess.KNIGHT, chess.BISHOP]:
                score += 0.4  # Increased development bonus
        
        # Bonus for castling (reduced for aggressive play)
        if board.is_castling(move):
            score += 0.2  # Reduced castling bonus for more aggressive play
        
        # Bonus for check (increased for aggressive play)
        if board.gives_check(move):
            score += 0.8  # Increased check bonus
        
        # Bonus for attacking squares near enemy king (increased)
        enemy_king = board.king(not board.turn)
        if enemy_king is not None:
            king_distance = abs(move.to_square % 8 - enemy_king % 8) + abs(move.to_square // 8 - enemy_king // 8)
            if king_distance <= 3:
                score += 0.6  # Increased king attack bonus
            elif king_distance <= 5:
                score += 0.3  # Medium distance attack bonus
        
        # Bonus for attacking moves (new aggressive feature)
        # Check if move attacks enemy pieces
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.color != board.turn:  # Enemy piece
                # Check if our move attacks this piece
                if move.to_square == square:
                    score += 0.5  # Direct attack bonus
                # Check if move creates discovered attacks
                elif move.from_square != square:
                    # Simple discovered attack detection
                    score += 0.2  # Discovered attack bonus
        
        # Bonus for pawn advancement (aggressive)
        piece = board.piece_at(move.from_square)
        if piece and piece.piece_type == chess.PAWN:
            if board.turn:  # White pawns
                if move.to_square // 8 > move.from_square // 8:  # Moving forward
                    score += 0.3
            else:  # Black pawns
                if move.to_square // 8 < move.from_square // 8:  # Moving forward
                    score += 0.3
        
        # Bonus for queen activity (aggressive)
        if piece and piece.piece_type == chess.QUEEN:
            score += 0.4  # Queen activity bonus
        
        # Penalty for moving the same piece repeatedly (reduced for aggressive play)
        if game_state.ai_last_moves and move.from_square == game_state.ai_last_moves[-1].from_square:
            score -= 0.1  # Reduced penalty for aggressive play
        
        # Bonus for tactical opportunities
        if board.gives_check(move):
            # Check if check leads to mate or winning position
            board.push(move)
            if board.is_checkmate():
                score += 10.0  # Mate bonus
            elif board.is_check():
                score += 0.5  # Double check bonus
            board.pop()
        
        move_scores.append((move, score))
    
    # Sort by score and add some randomness to top moves
    move_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Select from top 3 moves with some randomness (more aggressive selection)
    top_moves = move_scores[:min(3, len(move_scores))]
    if len(top_moves) > 1:
        # Add randomness to top moves (more weight to best move)
        weights = [1.0, 0.5, 0.2]  # More weight to best move for aggressive play
        total_weight = sum(weights[:len(top_moves)])
        rand = random.random() * total_weight
        
        cumulative_weight = 0
        for i, (move, score) in enumerate(top_moves):
            cumulative_weight += weights[i]
            if rand <= cumulative_weight:
                return move
    
    return move_scores[0][0] if move_scores else random.choice(legal_moves)

def main():
    """Enhanced main game loop"""
    welcome_menu()
    difficulty = level_selection_menu()
    
    game_state = GameState()
    game_state.difficulty = difficulty
    buttons = create_buttons()
    
    clock = pygame.time.Clock()
    running = True
    
    print(f"Game started with difficulty: {difficulty}")
    
    while running:
        # Update animation time
        if game_state.animation_time < game_state.animation_duration:
            game_state.animation_time += clock.get_time() / 1000.0
        
        # Draw everything
        draw_board()
        highlight_squares(game_state.board, game_state)
        draw_pieces(game_state.board, game_state)
        draw_panel(game_state)
        
        # Draw buttons
        for button in buttons:
            button.draw(WINDOW)
        
        pygame.display.flip()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle button events first
            button_clicked = False
            for button in buttons:
                if button.handle_event(event):
                    button_clicked = True
                    print(f"Button clicked: {button.text}")  # Debug info
                    if button.text == "New Game":
                        game_state = GameState()
                        game_state.difficulty = difficulty
                        game_state.animation_time = 0
                        print("New game started")
                    elif button.text == "Reset":
                        game_state.board = chess.Board()
                        game_state.selected_square = None
                        game_state.move_history = []
                        game_state.ai_last_moves = []  # Clear AI move history
                        game_state.game_over = False
                        game_state.winner = None
                        game_state.current_player = "White"
                        game_state.last_move = None
                        game_state.animation_time = 0
                        print("Game reset")
                    elif button.text == "Undo":
                        if len(game_state.move_history) > 0:
                            # Remove the last move from history
                            game_state.move_history.pop()
                            # Reset the board and replay all moves except the last one
                            game_state.board = chess.Board()
                            for move_obj, san_move in game_state.move_history:
                                game_state.board.push(move_obj)
                            game_state.current_player = "White" if game_state.board.turn == chess.WHITE else "Black"
                            game_state.last_move = None
                            game_state.animation_time = 0
                            print("Move undone")
                    elif button.text == "Settings":
                        # Show difficulty selection again
                        new_difficulty = level_selection_menu()
                        game_state.difficulty = new_difficulty
                        print(f"Difficulty changed to: {new_difficulty}")
                    break  # Only handle one button click at a time
            
            # Handle mouse clicks for chess moves (only if no button was clicked)
            if event.type == pygame.MOUSEBUTTONDOWN and not game_state.game_over and not button_clicked:
                if game_state.board.turn == chess.WHITE:
                    mouse_pos = pygame.mouse.get_pos()
                    move_done, new_selected, move, san_move = handle_user_move(
                        game_state.board, mouse_pos, game_state.selected_square
                    )
                    
                    if move_done and move and san_move:
                        game_state.move_history.append((move, san_move))
                        game_state.last_move = move
                        game_state.animation_time = 0
                        game_state.current_player = "Black"
                        print(f"Player moved: {san_move}")
                    
                    game_state.selected_square = new_selected
        
        # AI move
        if game_state.board.turn == chess.BLACK and not game_state.game_over:
            pygame.time.wait(500)  # Small delay for better UX
            
            if game_state.difficulty == "easy":
                move = random.choice(list(game_state.board.legal_moves))
            elif game_state.difficulty == "medium":
                # Simple evaluation-based move
                best_move = None
                best_score = float('-inf')
                for move in game_state.board.legal_moves:
                    game_state.board.push(move)
                    score = evaluate_board(game_state.board)
                    game_state.board.pop()
                    if score > best_score:
                        best_score = score
                        best_move = move
                move = best_move or random.choice(list(game_state.board.legal_moves))
            elif game_state.difficulty == "hard":
                # Enhanced AI with smart move selection and anti-repetition
                # Try opening book first for early game
                if len(game_state.move_history) < 6:
                    opening_move = get_opening_move(game_state.board)
                    if opening_move:
                        move = opening_move
                    else:
                        move = get_smart_ai_move(game_state.board, game_state)
                else:
                    move = get_smart_ai_move(game_state.board, game_state)
                
                # Track AI moves to prevent repetition
                game_state.ai_last_moves.append(move)
                if len(game_state.ai_last_moves) > 6:  # Keep only last 6 moves
                    game_state.ai_last_moves.pop(0)
            
            # Get the SAN notation before pushing the move
            san_move = game_state.board.san(move)
            game_state.board.push(move)
            game_state.move_history.append((move, san_move))
            game_state.last_move = move
            game_state.animation_time = 0
            game_state.current_player = "White"
            print(f"AI move: {san_move}")
        
        # Check game state
        if game_state.board.is_game_over():
            game_state.game_over = True
            if game_state.board.is_checkmate():
                game_state.winner = "Black" if game_state.board.turn == chess.WHITE else "White"
            elif game_state.board.is_stalemate():
                game_state.winner = "Draw"
        
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main() 

import pygame
import chess
import random
import time

# Initialize Pygame
pygame.init()

# Constants
BOARD_SIZE = 600
SQUARE_SIZE = BOARD_SIZE // 8
WHITE = (240, 217, 181)
BLACK = (181, 136, 99)
HIGHLIGHT_COLOR_SELECTED = (0, 255, 0, 128)  # Green
HIGHLIGHT_COLOR_MOVES = (0, 0, 255, 128)  # Blue
WINDOW = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
pygame.display.set_caption("Chess Game")
FONT = pygame.font.Font(pygame.font.match_font("arial"), 36)

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


# Draw the chessboard
def draw_board():
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(
                WINDOW,
                color,
                (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
            )


# Draw pieces
def draw_pieces(board):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            col = square % 8
            row = square // 8
            WINDOW.blit(PIECES[str(piece)], (col * SQUARE_SIZE, row * SQUARE_SIZE))


# Highlight selected piece and its possible moves
def highlight_moves(board, selected_square):
    if selected_square is not None:
        col = selected_square % 8
        row = selected_square // 8
        pygame.draw.rect(
            WINDOW,
            HIGHLIGHT_COLOR_SELECTED,
            (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
            0,
        )

        for move in board.legal_moves:
            if move.from_square == selected_square:
                to_col = move.to_square % 8
                to_row = move.to_square // 8
                pygame.draw.rect(
                    WINDOW,
                    HIGHLIGHT_COLOR_MOVES,
                    (
                        to_col * SQUARE_SIZE,
                        to_row * SQUARE_SIZE,
                        SQUARE_SIZE,
                        SQUARE_SIZE,
                    ),
                    0,
                )


# Handle user move
def handle_user_move(board, mouse_pos, selected_square):
    col = mouse_pos[0] // SQUARE_SIZE
    row = mouse_pos[1] // SQUARE_SIZE
    square = row * 8 + col
    # If a piece is selected
    if selected_square is not None:
        move = chess.Move(selected_square, square)

        piece = board.piece_at(selected_square)
        if piece and piece.piece_type == chess.PAWN:
            print(chess.square_rank(selected_square))
            print(chess.square_rank(selected_square))
            if (piece.color and chess.square_rank(selected_square) == 6) or (
                not piece.color and chess.square_rank(selected_square) == 1
            ):
                promotion_piece = prompt_for_promotion(piece.color)
                if promotion_piece:
                    move.promotion = promotion_piece.piece_type

        if move in board.legal_moves:
            board.push(move)
            return True, None  # Move done, deselect
        else:
            # If the same piece is clicked again, deselect it
            if selected_square == square:
                return False, None  # Deselect
            # If a different piece is clicked, select it
            elif board.piece_at(square) and board.piece_at(square).color == board.turn:
                return False, square  # Select new piece
            return False, selected_square  # Keep the current selection

    # If no piece is selected, select a new piece
    if board.piece_at(square) and board.piece_at(square).color == board.turn:
        return False, square  # Select new piece

    return False, None  # No valid action


# AI move logic using MCTS
def ai_move_mcts(board, time_limit=5):
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


# Evaluate board
def evaluate_board(board):
    values = {
        "P": 1,
        "N": 3,
        "B": 3,
        "R": 5,
        "Q": 9,
        "K": 0,
        "p": -1,
        "n": -3,
        "b": -3,
        "r": -5,
        "q": -9,
        "k": 0,
    }
    eval = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            eval += values[str(piece)]
    return eval


# Function to handle pawn promotion
def handle_pawn_promotion(board, selected_square):
    piece = board.piece_at(selected_square)
    if piece and piece.piece_type == chess.PAWN:
        if (piece.color and chess.square_rank(selected_square) == 7) or (
            not piece.color and chess.square_rank(selected_square) == 0
        ):
            # Prompt for promotion choice
            promotion_piece = prompt_for_promotion(piece.color)
            if promotion_piece:
                board.set_piece_at(selected_square, promotion_piece)


# Function to prompt user for promotion choice
def prompt_for_promotion(color):
    # Display promotion options
    WINDOW.fill((255, 223, 186))  # Light background color
    title_text = FONT.render("Promote Pawn", True, (0, 0, 0))
    queen_text = FONT.render("Press 'Q' for Queen", True, (0, 0, 0))
    rook_text = FONT.render("Press 'R' for Rook", True, (0, 0, 0))
    bishop_text = FONT.render("Press 'B' for Bishop", True, (0, 0, 0))
    knight_text = FONT.render("Press 'N' for Knight", True, (0, 0, 0))

    # Center the text
    title_rect = title_text.get_rect(center=(BOARD_SIZE // 2, BOARD_SIZE // 4))
    queen_rect = queen_text.get_rect(center=(BOARD_SIZE // 2, BOARD_SIZE // 2))
    rook_rect = rook_text.get_rect(center=(BOARD_SIZE // 2, BOARD_SIZE // 2 + 50))
    bishop_rect = bishop_text.get_rect(center=(BOARD_SIZE // 2, BOARD_SIZE // 2 + 100))
    knight_rect = knight_text.get_rect(center=(BOARD_SIZE // 2, BOARD_SIZE // 2 + 150))

    # Draw the text
    WINDOW.blit(title_text, title_rect)
    WINDOW.blit(queen_text, queen_rect)
    WINDOW.blit(rook_text, rook_rect)
    WINDOW.blit(bishop_text, bishop_rect)
    WINDOW.blit(knight_text, knight_rect)
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


# Welcome menu
def welcome_menu():
    WINDOW.fill((255, 223, 186))  # Light background color
    title_text = FONT.render("Welcome to Chess Game", True, (0, 0, 0))
    start_text = FONT.render(" Press 'S' to Start", True, (0, 0, 0))
    quit_text = FONT.render("Press 'Q' to Quit", True, (0, 0, 0))

    # Center the text
    title_rect = title_text.get_rect(center=(BOARD_SIZE // 2, BOARD_SIZE // 4))
    start_rect = start_text.get_rect(center=(BOARD_SIZE // 2, BOARD_SIZE // 2))
    quit_rect = quit_text.get_rect(center=(BOARD_SIZE // 2, BOARD_SIZE // 2 + 50))

    # Draw the text
    WINDOW.blit(title_text, title_rect)
    WINDOW.blit(start_text, start_rect)
    WINDOW.blit(quit_text, quit_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    return  # Start the game
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()


# Difficulty level selection menu
def level_selection_menu():
    WINDOW.fill((255, 223, 186))  # Light background color
    title_text = FONT.render("Select Difficulty Level", True, (0, 0, 0))
    easy_text = FONT.render("1. Easy", True, (0, 0, 0))
    medium_text = FONT.render("2. Medium", True, (0, 0, 0))
    hard_text = FONT.render("3. Hard", True, (0, 0, 0))

    # Center the text
    title_rect = title_text.get_rect(center=(BOARD_SIZE // 2, BOARD_SIZE // 4))
    easy_rect = easy_text.get_rect(center=(BOARD_SIZE // 2, BOARD_SIZE // 2))
    medium_rect = medium_text.get_rect(center=(BOARD_SIZE // 2, BOARD_SIZE // 2 + 50))
    hard_rect = hard_text.get_rect(center=(BOARD_SIZE // 2, BOARD_SIZE // 2 + 100))

    # Draw the text
    WINDOW.blit(title_text, title_rect)
    WINDOW.blit(easy_text, easy_rect)
    WINDOW.blit(medium_text, medium_rect)
    WINDOW.blit(hard_text, hard_rect)
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


# Main game loop
def main():
    welcome_menu()  # Show welcome menu
    level = level_selection_menu()
    board = chess.Board()
    running = True
    selected_square = None

    print(
        "Game started with difficulty:", level
    )  # Print the level selection once at the start

    while running:
        draw_board()
        highlight_moves(board, selected_square)
        draw_pieces(board)
        pygame.display.update()  # Use update instead of flip for completeness

        # Debugging print when each piece move happens
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Exiting the game.")
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and board.turn == chess.WHITE:
                mouse_pos = pygame.mouse.get_pos()
                move_done, selected_square = handle_user_move(
                    board, mouse_pos, selected_square
                )
                if move_done and selected_square is not None:
                    print(
                        f"Player moved: {board.san(board.peek())}"
                    )  # Display the move in SAN format

        if board.turn == chess.BLACK:
            if level == "easy":
                move = random.choice(list(board.legal_moves))
            elif level == "medium":
                move = random.choice(list(board.legal_moves))  # Placeholder for minimax
            elif level == "hard":
                move = ai_move_mcts(board, time_limit=5)

            print(f"AI ({'Black'}) move: {board.san(move)}")  # Print AI move
            board.push(move)
            handle_pawn_promotion(board, move.to_square)

    pygame.quit()


# Start the game
if __name__ == "__main__":
    main()
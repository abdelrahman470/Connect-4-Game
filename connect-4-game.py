import random
import math
import copy

# ---------------------------------------------------------
# GAME CONFIGURATION AND CONSTANTS
# ---------------------------------------------------------
ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER_PIECE = 'X'
AI_PIECE = 'O'
EMPTY = '-'

WINDOW_LENGTH = 4

# Depth determines how many moves ahead the AI calculates.
SEARCH_DEPTH = 4

# ---------------------------------------------------------
# BOARD MANAGEMENT FUNCTIONS
# ---------------------------------------------------------


def create_board():
    """Initializes a 6x7 grid filled with zeros."""
    board = [[EMPTY for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]
    return board


def drop_piece(board, row, col, piece):
    """Updates the board matrix with the player's piece at the specific location."""
    board[row][col] = piece


def is_valid_location(board, col):
    """Checks if the selected column has space available (top row is empty)."""
    return board[ROW_COUNT - 1][col] == EMPTY


def get_next_open_row(board, col):
    """Finds the lowest empty row in a column (simulates gravity)."""
    for r in range(ROW_COUNT):
        if board[r][col] == EMPTY:
            return r


def print_board(board):
    """
    Prints the board to the console.
    We iterate in reverse order so the visual board matches gravity (row 0 at bottom).
    """
    print("\n  0 1 2 3 4 5 6")
    print("----------------")
    for row in reversed(board):
        print("| " + " ".join(str(x) for x in row) + " |")
    print("----------------")


def get_valid_locations(board):
    """Returns a list of all column indices that are valid to play in."""
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def winning_move(board, piece):
    """
    Scans the entire board to check if the given piece has won.
    Returns True if there are 4 connected pieces.
    """
    # 1. Check Horizontal locations
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # 2. Check Vertical locations
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # 3. Check Positively Sloped Diagonals (/)
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # 4. Check Negatively Sloped Diagonals (\)
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    return False


def is_terminal_node(board):
    """Checks if the game has ended (Win for Player, Win for AI, or Draw)."""
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

# ---------------------------------------------------------
# SCORING ALGORITHMS (HEURISTICS)
# ---------------------------------------------------------


def evaluate_window(window, piece):
    """
    Assigns a score to a specific set of 4 cells (a window).
    This logic helps the AI decide which move is better when not at a winning state.
    """
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    # Priority 1: Connect 4 (Win)
    if window.count(piece) == 4:
        score += 100
    # Priority 2: Connect 3 with one empty spot (Attack)
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    # Priority 3: Connect 2 with two empty spots (Setup)
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    # Priority 4: Block Opponent (Defense)
    # If the opponent has 3 pieces and 1 empty spot, penalize heavily to encourage blocking.
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


def score_position(board, piece):
    """
    Calculates the total score of the board for the AI.
    It sums up the scores of all horizontal, vertical, and diagonal windows.
    """
    score = 0

    # Preference: Center Column
    # Controlling the center is strategically better in Connect 4.
    center_array = [i[COLUMN_COUNT // 2] for i in board]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score Horizontal
    for r in range(ROW_COUNT):
        row_array = board[r]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [row[c] for row in board]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score Positive Diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Score Negative Diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

# ---------------------------------------------------------
# MINIMAX ALGORITHM
# ---------------------------------------------------------


def minimax(board, depth, maximizingPlayer):
    """
    The main Minimax algorithm.
    It recursively simulates future moves to find the best possible outcome.
    """
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    # Base Case: Stop recursion if game over or depth limit reached
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)  # AI Wins
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)  # Player Wins
            else:
                return (None, 0)  # Draw
        else:
            # Depth is zero: return the heuristic score of the current board state
            return (None, score_position(board, AI_PIECE))

    # Maximizing Player Logic (AI)
    # The AI tries to maximize the score.
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)

        for col in valid_locations:
            row = get_next_open_row(board, col)

            # Create a copy of the board to simulate the move
            b_copy = copy.deepcopy(board)
            drop_piece(b_copy, row, col, AI_PIECE)

            # Recursive call
            new_score = minimax(b_copy, depth-1, False)[1]

            # Check if this move is better than what we found so far
            if new_score > value:
                value = new_score
                column = col

        return column, value

    # Minimizing Player Logic (Human)
    # The AI assumes the Human plays perfectly to minimize the AI's score.
    else:
        value = math.inf
        column = random.choice(valid_locations)

        for col in valid_locations:
            row = get_next_open_row(board, col)

            # Create a copy of the board to simulate the move
            b_copy = copy.deepcopy(board)
            drop_piece(b_copy, row, col, PLAYER_PIECE)

            # Recursive call
            new_score = minimax(b_copy, depth-1, True)[1]

            # Check if this move is worse for the AI (better for Human)
            if new_score < value:
                value = new_score
                column = col

        return column, value

# ---------------------------------------------------------
# MAIN GAME LOOP
# ---------------------------------------------------------


def play_game():
    board = create_board()
    game_over = False
    turn = random.randint(0, 1)  # Randomize who starts

    print("=== CONNECT 4 CONSOLE GAME ===")
    print(f"Human (Player 1) vs AI (Player 2)")
    print_board(board)

    while not game_over:

        # --- Human Turn ---
        if turn == 0:
            try:
                user_input = input(
                    f"Player 1 Turn (Select Column 0-{COLUMN_COUNT-1}): ")

                if not user_input.isnumeric():
                    print("Please enter a valid number.")
                    continue

                col = int(user_input)

                if col < 0 or col > COLUMN_COUNT-1:
                    print("Invalid column number.")
                    continue

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):
                        print_board(board)
                        print("CONGRATULATIONS! PLAYER 1 WINS!")
                        game_over = True

                    turn += 1
                    turn = turn % 2
                    print_board(board)
                else:
                    print("Column is full. Pick another one.")

            except ValueError:
                print("Error processing input.")

        # --- AI Turn ---
        else:
            print("AI is calculating best move...")

            # Run Minimax to determine the best column
            col, minimax_score = minimax(board, SEARCH_DEPTH, True)

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if winning_move(board, AI_PIECE):
                    print_board(board)
                    print("GAME OVER. AI WINS!")
                    game_over = True

                print_board(board)
                turn += 1
                turn = turn % 2

    print("Game Finished.")


if __name__ == "__main__":
    play_game()

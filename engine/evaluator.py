import chess
from .minimax import minimax

def choose_move(board: chess.Board, depth: int = 2) -> chess.Move:
    """
    Choose the best move for the current player using minimax.
    """

    best_move = None
    is_maximizing = board.turn == chess.WHITE
    best_score = -float("inf") if is_maximizing else float("inf")

    for move in board.legal_moves:
        board.push(move)
        score = minimax(board, depth - 1, not is_maximizing)
        board.pop()

        if is_maximizing and score > best_score:
            best_score, best_move = score, move
        elif not is_maximizing and score < best_score:
            best_score, best_move = score, move

    return best_move

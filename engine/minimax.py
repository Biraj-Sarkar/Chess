import chess
from ml import evaluate_board

def minimax(board: chess.Board, depth: int, is_maximizing: bool) -> float:
    """
    Minimax search using ML evaluation.
    """

    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if is_maximizing:
        best = -float("inf")
        for move in board.legal_moves:
            board.push(move)
            best = max(best, minimax(board, depth - 1, False))
            board.pop()
        return best
    else:
        best = float("inf")
        for move in board.legal_moves:
            board.push(move)
            best = min(best, minimax(board, depth - 1, True))
            board.pop()
        return best

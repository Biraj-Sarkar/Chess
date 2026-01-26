import chess
import time
from engine.minimax import negamax

def choose_move(board: chess.Board, max_time: float = 1.0):
    start = time.time()
    best_move = None
    depth = 1

    while True:
        if time.time() - start > max_time:
            break

        best_score = -float("inf")
        for move in board.legal_moves:
            board.push(move)
            score = -negamax(board, depth - 1, -1e9, 1e9)
            board.pop()

            if score > best_score:
                best_score = score
                best_move = move

        depth += 1

    return best_move
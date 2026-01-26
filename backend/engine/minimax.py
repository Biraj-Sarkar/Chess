import chess
from ml import evaluate_fen
from utils import normalize_fen

INF = float("inf")
TT = {}

PIECE_VALUES = {
    chess.PAWN: 0.1,
    chess.KNIGHT: 0.3,
    chess.BISHOP: 0.3,
    chess.ROOK: 0.5,
    chess.QUEEN: 0.9,
}

def ordered_moves(board: chess.Board):
    captures = []
    quiets = []
    
    for move in board.legal_moves:
        if board.is_capture(move):
            captures.append(move)
        else:
            quiets.append(move)

    return captures + quiets

def quiescence(board, alpha, beta):
    stand_pat = evaluate_fen(board.fen())

    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    for move in board.legal_moves:
        if not board.is_capture(move):
            continue

        board.push(move)
        score = -quiescence(board, -beta, -alpha)
        board.pop()

        if score >= beta:
            return beta
        if score > alpha:
            alpha = score

    return alpha

def negamax(board, depth, alpha, beta):
    key = normalize_fen(board.fen())
    if key in TT and TT[key][0] >= depth:
        return TT[key][1]

    if board.is_game_over():
        result = board.result()
        if result == "1-0":
            return 1.0
        elif result == "0-1":
            return -1.0
        else:
            return 0.0

    if depth == 0:
        return quiescence(board, alpha, beta)

    best = -INF
    for move in ordered_moves(board):
        board.push(move)
        score = -negamax(board, depth - 1, -beta, -alpha)
        board.pop()

        best = max(best, score)
        alpha = max(alpha, best)

        if alpha >= beta:
            break

    TT[key] = (depth, best)
    return best
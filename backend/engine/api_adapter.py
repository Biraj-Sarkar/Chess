import chess
from engine.evaluator import choose_move

def play_move(fen: str, move_uci: str, max_time: float = 1.0) -> dict:
    """
    Plays one human move and one AI move.

    Args:
        fen (str): Current board position in FEN format
        move_uci (str): Human move in UCI format (e.g. 'e2e4')
        depth (int): Minimax depth for AI

    Returns:
        dict: {
            'fen': str,
            'human_move': str,
            'ai_move': str | None,
            'game_over': bool,
            'result': str | None
        }
    """
    board = chess.Board(fen)

    # ---------------------------
    # Human move
    # ---------------------------
    try:
        human_move = chess.Move.from_uci(move_uci)
    except ValueError:
        raise ValueError("Invalid UCI move format")
    
    if human_move not in board.legal_moves:
        raise ValueError("Illegal move")
    
    board.push(human_move)

    if board.is_game_over() :
        return board.fen(), None
    
    # ---------------------------
    # AI move
    # ---------------------------
    ai_move = choose_move(board, max_time)  # 1 second

    if ai_move is not None:
        board.push(ai_move)

    return board.fen(), ai_move.uci()
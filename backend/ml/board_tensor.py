import chess
import numpy as np

# Piece type mapping for python-chess
piece_map = {
    chess.PAWN: 0,
    chess.KNIGHT: 1,
    chess.BISHOP: 2,
    chess.ROOK: 3,
    chess.QUEEN: 4,
    chess.KING: 5
}

# Total planes:
# 12 piece planes
# 1 side-to-move
# 4 castling rights
# 1 en-passant
TOTAL_PLANES = 17

def board_to_tensor(board: chess.Board) -> np.ndarray:
    tensor = np.zeros((8, 8, TOTAL_PLANES), dtype=np.float32)    

    # Iterate through all squares
    for square, piece in board.piece_map().items():
        if piece is not None:
            rank = 7 - (square // 8)
            file = square % 8

            offset = 0 if piece.color == chess.WHITE else 6
            plane = piece_map[piece.piece_type] + offset
            tensor[rank, file, plane] = 1.0
    
    # Side to move
    tensor[:, :, 12] = 1.0 if board.turn == chess.WHITE else 0.0

    # Planes 13-16: Castling rights
    if board.has_kingside_castling_rights(chess.WHITE):
        tensor[:, :, 13] = 1.0
    
    if board.has_queenside_castling_rights(chess.WHITE):
        tensor[:, :, 14] = 1.0
    
    if board.has_kingside_castling_rights(chess.BLACK):
        tensor[:, :, 15] = 1.0
    
    if board.has_queenside_castling_rights(chess.BLACK):
        tensor[:, :, 16] = 1.0

    # ep = board.ep_square
    # if ep is not None:
    #     rank = 7 - (ep // 8)
    #     file = ep % 8
    #     tensor[rank, file, 17] = 1.0

    return tensor
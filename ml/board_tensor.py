import chess
import numpy as np

def board_to_tensor(board: chess.Board) -> np.ndarray:
    """
    Input: chess.Board
    Output: numpy array of shape (8, 8, 17)
    """
    tensor = np.zeros((8, 8, 17), dtype=np.float32)

    # Piece type mapping for python-chess
    piece_map = {
        chess.PAWN: 0,
        chess.KNIGHT: 1,
        chess.BISHOP: 2,
        chess.ROOK: 3,
        chess.QUEEN: 4,
        chess.KING: 5
    }

    # Iterate through all squares
    for square in chess.SQUARES:
        piece = board.piece_at(square)

        if piece is not None:
            rank = 7 - (square // 8)
            file = square % 8

            piece_type_idx = piece_map[piece.piece_type]

            plane = piece_type_idx
            if piece.color == chess.BLACK:
                plane += 6

            tensor[rank, file, plane] = 1
    
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

    return tensor
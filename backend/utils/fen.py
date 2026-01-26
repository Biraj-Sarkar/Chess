def normalize_fen(fen: str) -> str:
    """
    Normalize FEN for caching and transposition table.
    Keeps only:
    - piece placement
    - side to move
    - castling rights
    - en-passant square
    """
    return " ".join(fen.split()[:4])

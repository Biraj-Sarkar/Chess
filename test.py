import chess
from engine import choose_move

board = chess.Board()
move = choose_move(board, depth=2)
print(move)
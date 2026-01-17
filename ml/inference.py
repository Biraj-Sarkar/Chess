import os
import numpy as np
import chess
import tensorflow as tf
from .board_tensor import board_to_tensor

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "chess_cnn_evaluator.keras")
model = tf.keras.models.load_model(MODEL_PATH)

def evaluate_board(board: chess.Board) -> float:
    """
    Returns a numeric evaluation of the position.
    Positive → White better
    Negative → Black better
    """

    tensor = board_to_tensor(board)
    tensor = np.expand_dims(tensor, axis=0)

    probs = model.predict(tensor, verbose=0)[0]

    # Black better = -1, Equal = 0, White better = +1
    score = probs[2] - probs[0]

    return score
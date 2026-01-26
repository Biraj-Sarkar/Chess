import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import threading
import numpy as np
import chess
import tensorflow as tf
from functools import lru_cache
from .board_tensor import board_to_tensor
from utils import normalize_fen

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "chess_cnn_evaluator.keras")

_model = None
_model_lock = threading.Lock()
_predict_lock = threading.Lock()

def _load_model():
    global _model
    if _model is None:
        with _model_lock:
            if _model is None:
                _model = tf.keras.models.load_model(MODEL_PATH)
    return _model

@lru_cache(maxsize=20000)
def _evaluate_cached(norm_fen: str) -> float:
    board = chess.Board(norm_fen)
    tensor = np.expand_dims(board_to_tensor(board), axis=0)

    model = _load_model()
    with _predict_lock:
        value = model.predict(tensor, verbose=0)[0][0]

    return float(value)

def evaluate_fen(fen: str) -> float:
    return _evaluate_cached(normalize_fen(fen))
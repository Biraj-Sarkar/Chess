# ml/__init__.py
from .board_tensor import board_to_tensor
from .inference import evaluate_fen

__all__ = ["board_to_tensor", "evaluate_fen"]
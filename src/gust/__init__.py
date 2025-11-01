"""
GUST - Genetic Universal Stockfish Trainer

A Python-based AI project for training and optimizing Stockfish chess engine
using genetic algorithms.
"""

__version__ = "0.1.0"
__author__ = "Laurent Aerens"

from . import genetic
from . import trainer
from . import evaluator
from . import utils

__all__ = ["genetic", "trainer", "evaluator", "utils"]

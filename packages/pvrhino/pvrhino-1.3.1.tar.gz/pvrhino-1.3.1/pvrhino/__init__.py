from .binding.python.rhino import Rhino
from .resources.util.python import *


def create(context_path, library_path=None, model_path=None, sensitivity=0.5):
    """
    Factory method for Rhino Speech-to-Intent engine.

    :param context_path: Absolute path to file containing context parameters. A context represents the set of
    expressions (spoken commands), intents, and intent arguments (slots) within a domain of interest.
    :param library_path: Absolute path to Rhino's dynamic library.
    :param model_path: Absolute path to file containing model parameters.
    :param sensitivity: Inference sensitivity. It should be a number within [0, 1]. A higher sensitivity value results
    in fewer misses at the cost of (potentially) increasing the erroneous inference rate.
    :return: An instance of Rhino Speech-to-Intent engine.
    """

    if library_path is None:
        library_path = LIBRARY_PATH

    if model_path is None:
        model_path = MODEL_PATH

    return Rhino(library_path=library_path, model_path=model_path, context_path=context_path, sensitivity=sensitivity)

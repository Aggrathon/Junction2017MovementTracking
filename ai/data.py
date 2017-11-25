"""
    Datamanagement
"""
import numpy as np
from model import PREDS

def get_data():
    """
        Get data samples for training
    """
    #TODO read files
    #TODO find footsteps
    #TODO create sequences
    return [(np.zeros([200, 12], np.float), np.zeros([PREDS], np.float)) for _ in range(100)]

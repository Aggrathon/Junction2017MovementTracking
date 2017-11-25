"""
    Datamanagement
"""
import numpy as np
from model import PREDS

def get_data():
    """
        Get data samples for training
    """
    data = [] 
    for file in []: #TODO read files
        f, label = read_file(file)
        start = get_next_step(f, 0)
        stop = get_next_step(f, start)
        while stop > 0:
            data.append((f[start:stop], label)
            start = stop
    data = [(np.zeros([200, 12], np.float), np.zeros([PREDS], np.float)) for _ in range(100)] #TODO remove
    return data

def get_next_step(data, start):
    """
        Find the next footstep
    """
    for i in range(start, len(data)):
        if data[i]: #TODO find footstep
            return i
    return -1

def read_file(file):
    return [], [] #TODO read data

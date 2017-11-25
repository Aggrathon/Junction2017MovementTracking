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
    for file in ["data/data.csv"]:
        label = [0]
        time, data = read_file(file)
        smooth = data_smooth(data)
        start = get_next_step(smooth, 0)
        stop = get_next_step(smooth, start)
        while stop > 0:
            data.append((data[start:stop], label))
            start = stop
            stop = get_next_step(smooth, start)
    data = [(np.zeros([200, 12], np.float), np.zeros([PREDS], np.float)) for _ in range(100)] #TODO remove
    return data

def get_next_step(data, start):
    """
        Find the next footstep
    """
    start = max(start+1, 3)
    for i in range(start, len(data)-3):
        grt = True
        for j in range(-3, 8):
            if data[i] < data[i+j]:
                grt = False
                break
        if grt:
            return i
    return -1

def read_file(filename):
    """
        Read a csv
    """
    time = []
    x = []
    y = []
    z = []
    with open(filename) as file:
        file.readline()
        for l in file.readlines():
            split = l[:-1].split(',')
            time.append(float(split[0]))
            x.append(float(split[1]))
            y.append(float(split[2]))
            z.append(float(split[3]))
    return time, [x, y, z]

def data_abs(data):
    return np.abs(data[0]) + np.abs(data[1]) + np.abs(data[2])

def data_smooth(data):
    abs = data_abs(data)
    smooth = abs[0:-6]+abs[1:-5]*2+abs[2:-4]*4+abs[3:-3]*4+abs[4:-2]*2+abs[5:-1]
    smooth = np.concatenate(([0,0,0], smooth, [0,0,0]))
    return smooth

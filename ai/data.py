"""
    Datamanagement
"""
import os
import numpy as np
from model import PREDS

def get_data(files=None):
    """
        Get data samples for training
    """
    if files is None:
        files = ['data/'+file for file in os.listdir('data')]
    data_all = []
    for file in files:
        if 'fix' not in file or 'csv' not in file:
            continue
        label = [0 for _ in range(PREDS)]
        if 'left' in file:
            label[1] = 1
        elif 'right' in file:
            label[2] = 1
        elif 'walk' in file:
            label[0] = 1
        time, data = read_file(file)
        smooth = data_smooth(data)
        start = get_next_step(smooth, 0)
        stop = get_next_step(smooth, start)
        while stop > 0:
            data_all.append((data[start:stop], label))
            start = stop
            stop = get_next_step(smooth, start)
    return data_all

def get_next_step(data, start):
    """
        Find the next footstep
    """
    start = max(start+1, 3)
    for i in range(start, len(data)-8):
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
    print('Reading: '+filename)
    time = []
    data = []
    with open(filename) as file:
        file.readline()
        for l in file.readlines():
            split = l[:-1].split(',')
            time.append(float(split[0]))
            data.append(list(map(float, split[1:])))
    return time, np.asarray(data)

def data_abs(data):
    abs = np.abs(data[:, 0])
    for i in range(1, data.shape[1]):
        abs += np.abs(data[:, i])
    return abs

def data_smooth(data):
    abs = data_abs(data)
    smooth = abs[0:-6]+abs[1:-5]*2+abs[2:-4]*4+abs[3:-3]*4+abs[4:-2]*2+abs[5:-1]
    smooth = np.concatenate(([0,0,0], smooth, [0,0,0]))
    return smooth

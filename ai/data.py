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
        label = [0.0 for _ in range(PREDS)]
        label[5] = 1.0
        if 'left' in file:
            label[1] = 1.0
        elif 'right' in file:
            label[2] = 1.0
        elif 'walk' in file:
            label[0] = 1.0
        elif 'stair' in file:
            if 'down' in file:
                label[4] = 1.0
            else:
                label[3] = 1.0
        elif 'halt' in file:
            label[0] = 1.0
        if 'jonas' in file:
            label[6] = 0.3
            label[5] = 0.7
        if '2b' in file or 'halt' in file:
            label[6] = 1.0
            label[5] = 0.0
        time, data = read_file(file)
        if len(time) < 10:
            continue
        smooth = data_smooth(data)
        start = get_next_step(smooth, 0)
        stop = get_next_step(smooth, start)
        while start > 0 and stop > 0:
            data_all.append((data[start-1:stop+1], label))
            start = stop
            stop = get_next_step(smooth, start)
    return data_all

def get_next_step(data, start):
    """
        Find the next footstep
    """
    start = max(start+2, 3)
    for i in range(start, len(data)-9):
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
    for i in range(0, min(4, data.shape[1])):
        abs += np.abs(data[:, i])
    return abs

def data_smooth(data):
    abs = data_abs(data)
    smooth = abs[0:-6]+abs[1:-5]*2+abs[2:-4]*4+abs[3:-3]*4+abs[4:-2]*2+abs[5:-1]
    smooth = np.concatenate(([0,0,0], smooth, [0,0,0]))
    return smooth


from matplotlib import pyplot as plt
import numpy as np
from data import read_file, data_abs, data_smooth, get_next_step

time, data = read_file('data/data.csv')
x = data[:, 0]
y = data[:, 1]
z = data[:, 2]
smooth = data_smooth(data)

plt.plot(time, z, 'b')
plt.plot(time, y, 'g')
plt.plot(time, x, 'r')
plt.plot(time, data_abs(data), 'purple')
plt.plot(time, smooth/12+10, 'black')

plt.show()

def plot_step_lengths(smooth, time):
    lengths = []
    start = get_next_step(smooth, 0)
    end = get_next_step(smooth, start)
    while end > 0:
        lengths.append(time[end]-time[start])
        start = end
        end = get_next_step(smooth, start)
    plt.plot(lengths)
    plt.show()

plot_step_lengths(smooth, time)

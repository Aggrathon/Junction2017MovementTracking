
from matplotlib import pyplot as plt
import numpy as np


time = []
x = []
y = []
z = []

with open('data/data.csv') as file:
    file.readline()
    for l in file.readlines():
        split = l[:-1].split(',')
        time.append(float(split[0]))
        x.append(float(split[1]))
        y.append(float(split[2]))
        z.append(float(split[3]))

abs = np.abs(x)+np.abs(y)+np.abs(z)
smooth = abs[0:-6]+abs[1:-5]*2+abs[2:-4]*4+abs[3:-3]*4+abs[4:-2]*2+abs[5:-1]
smooth = np.concatenate(([0,0,0], smooth/12+10, [0,0,0]))

plt.plot(time, z, 'b')
plt.plot(time, y, 'g')
plt.plot(time, x, 'r')
plt.plot(time, abs, 'purple')
plt.plot(time, smooth, 'black')

plt.show()

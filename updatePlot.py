import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import sys

try:
    FILE = sys.argv[1]
    print(FILE)
except:
    print("FUCK")

def animate(i, FILE = FILE):
    df = pd.read_csv(FILE)
    y = np.array(df['Frequency (GHz)'])
    Qraw = np.array(df['Q raw'])
    Qspline = np.array(df['Q spline'])
    x = range(len(y))
    ax1.cla()
    ax2.cla()
    ax1.plot(x, y, marker = 'o', color = 'darkolivegreen', label = 'Resonant Frequency')
    ax2.plot(x, Qraw, marker = 'o', color = 'cornflowerblue', label = 'Q raw')
    ax2.plot(x, Qspline, marker = 'D', color = 'darkcyan', label = 'Q spline')
    ax1.set_ylim(0.999*y.min(), 1.001*y.max())
    ax2.set_ylim(0.99*Qraw.min(), 1.01*Qraw.max())

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
plt.legend()
#plt.grid()

ani = FuncAnimation(plt.gcf(), animate, interval=5000, cache_frame_data=False)
plt.show()
#print(df)

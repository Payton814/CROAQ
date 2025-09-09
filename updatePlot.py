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
    #Qraw = np.array(df['Q raw'])
    Qspline = np.array(df['Q spline'])
    x = range(len(y))
    ax1.cla()
    ax2.cla()
    ax1.plot(x, y, marker = 'o', color = 'darkolivegreen', label = 'Resonant Frequency', alpha = 0.5)
    #ax2.plot(x, Qraw, marker = 'o', color = 'cornflowerblue', label = 'Q raw')
    ax2.plot(x, Qspline, marker = 'D', color = 'darkcyan', label = 'Q spline', alpha = 0.5)
    ax1.set_ylim(0.999*y.min(), 1.001*y.max())
    ax2.set_ylim(0.99*Qspline.min(), 1.01*Qspline.max())

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
#ax1.legend()
#ax2.legend()
#plt.grid()

ani = FuncAnimation(plt.gcf(), animate, interval=5000, cache_frame_data=False)
ax1.legend()
plt.show()
#print(df)

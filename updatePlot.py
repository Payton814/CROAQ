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
    x = range(len(y))
    plt.cla()
    plt.plot(x, y, marker = 'o')
    plt.ylim(0.999*y.min(), 1.001*y.max())

ani = FuncAnimation(plt.gcf(), animate, interval=5000, cache_frame_data=False)
plt.show()
#print(df)

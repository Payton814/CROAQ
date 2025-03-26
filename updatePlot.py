import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def animate(i):
    df = pd.read_csv('./test.csv')
    y = df['Data']
    x = range(len(y))
    plt.cla()
    plt.plot(x, y)

ani = FuncAnimation(plt.gcf(), animate, interval=1000, cache_frame_data=False)
plt.show()
#print(df)

import numpy as np
import matplotlib.pyplot as plt
from getS21 import getS21

f, s = getS21(1000, 1e9, 1.1e9, 32001, analyzer = 'N5230C')
plt.plot(f, s)
plt.show()

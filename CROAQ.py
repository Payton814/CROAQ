import matplotlib.pyplot as plt
from getS21_E5062A import getS21_E5062A
from getS21 import getS21
from getQraw import getQraw
from getQspline import getQspline
import pandas as pd
import numpy as np
from findPeaks import findPeak
import sys

## The E5062A is limited to 1601 sample points in a given bandwidth.
## Over the entire 1-3 GHz range, this means the sampling resolition is ~1.25 MHz.
## Assuming we can achieve a Q = 10000, the Full Width Half Maximum is 3e9/1e4 = 3e5 = 0.3 MHz.
## Severely undersampling to get an accurate Q.

## In hawaii on Peter's N5230C the number of points is 32001.
## Zooming in on a single peak, the sampling resolution was 3.125 kHz.
## 3.125kHz*1601 = 5 MHz.
## To get the same resolution on E5062A the bandwidth must be at most 5 MHz.
## This leaves a very small window for capturing the resonant peak and Q on E5062A.
## It can be done but every measurement the window will have to move and it has to move with the res peak.

## Q for a lossy material at full insertion was ~2000.
## 3GHz/2000 = 1.5 MHz. Therefore, 5 MHz should be enough to capture all realistic cases.

CURRENT_POS = float(sys.argv[1])
#IP = "192.168.2.233" ## IP address for the network analyzer in Beatty lab
IFBandwidth = 500 ## In Hz
WINDOW_WIDTH = 5.0e6
if (CURRENT_POS == 0):
    delf = 0
    fcent = findPeak(int(sys.argv[3]))
    fcent = findPeak(1, fl = fcent - 50e6, fu = fcent + 50e6, height = -45)
else:
    df = pd.read_csv('./data/' + sys.argv[2] + '/trial1.csv')
    flast = np.array(df['Frequency (GHz)'])[-1] ## Grab the resonant frequency fro last measurement
    if (CURRENT_POS > 1):
        flastlast = np.array(df['Frequency (GHz)'])[-2]
    else:
        flastlast = flast
    fcent = flast*1e9 ## The measurement window will be based around where the last peak was
    delf = abs(flastlast - flast)*1e9
                 

DEFAULT_SHIFT = 5e5
SHIFT = DEFAULT_SHIFT

## if the change in resonant frequency is larger than 50% of the
## the window width, increase it by 10%
if (delf > WINDOW_WIDTH/2):
    WINDOW_WIDTH = 4.0*delf
fstart = fcent -WINDOW_WIDTH/2 ## in Hz
fend = fcent + WINDOW_WIDTH/2 ## in Hz
nAVG = 1 ## Number of times the measurement is performed and averaged

print("Measurement Window: ", fstart, fend)

f, S21 = getS21(IFBandwidth, fstart, fend, 32001, 'N5230C')
Qraw = getQraw(f, S21)
try:
    Qspline = getQspline(f, 10**(S21/10))
except:
    Qspline = 0

Data = {'Frequency (Hz)': f,
        'S21': S21}

df = pd.DataFrame(Data)
df.to_csv('./data/' + sys.argv[2] + '/' + sys.argv[1] + '.csv', index=False, header=False)

fres = f[S21.argmax()]
print('Resonant Frequency', fres/1e9, "GHz")
Data2 = {'Step': [CURRENT_POS*75],
         'height (mm)': [CURRENT_POS*75*0.006],
         'Frequency (GHz)': [fres/1e9],
         'Qspline': [Qspline],
         'Qraw': [Qraw]}
df2 = pd.DataFrame(Data2)
df2.to_csv('./data/' + sys.argv[2] + '/trial1.csv', mode = 'a', index = False, header = False)

#print('Resonant Frequency', fres)
print('Q', Qraw, Qspline)
print("loss", S21.max())

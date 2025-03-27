import matplotlib.pyplot as plt
from getS21_E5062A import getS21_E5062A
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

CURRENT_POS = sys.argv[1]
IP = "192.168.2.233" ## IP address for the network analyzer in Beatty lab
IFBandwidth = 1e4 ## In Hz
DEFAULT_SHIFT = 1e6
WINDOW_WIDTH = 5e6 ## Window the VNA is taking measurements
fstart = 1e9 + WINDOW_WIDTH/2 ## in Hz
fend = 1e9 - WINDOW_WIDTH/2 ## in Hz
nAVG = 1 ## Number of times the measurement is performed and averaged

print("Measurement Window: ", fstart, fend)

S21 = getS21_E5062A(IP, IFBandwidth, fstart, fend, nAVG)
print("loss", S21[int(len(S21)/2)])

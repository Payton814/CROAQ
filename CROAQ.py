import matplotlib.pyplot as plt
from getS21_E5062A import getS21_E5062A

IP = "192.168.2.233" ## IP address for the network analyzer in Beatty lab
IFBandwidth = 1e4 ## In Hz
fstart = 1e9 ## in Hz
fend = 3e9 ## in Hz
nAVG = 1 ## Number of times the measurement is performed and averaged

S21 = getS21_E5062A(IP, IFBandwidth, fstart, fend, nAVG)
print("loss", S21[int(len(S21)/2)])

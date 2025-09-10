from pymeasure.instruments.agilent import AgilentE5062A
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import find_peaks
import sys
from getS21 import getS21


def findPeak(PeakNum, fl = 1e9, fu = 3e9, height = -45):## Establish a connection with the network analyzer
    ## Connection being established is through an ethernet cable between the Raspberry Pi and the VNA
    ## Since a LAN port is being used, the com type is TCPIP

    freqs, s_matrix = getS21('192.168.2.233', 100, fl, fu, 1601)

    peaks, _ = find_peaks(s_matrix, height=height)

    return freqs[peaks[PeakNum - 1]]

from pymeasure.instruments.agilent import AgilentE5062A
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import find_peaks
import sys


def findPeak(PeakNum, fl = 6e8, fu = 16e8, height = -50):## Establish a connection with the network analyzer
    ## Connection being established is through an ethernet cable between the Raspberry Pi and the VNA
    ## Since a LAN port is being used, the com type is TCPIP

## IP 192.168.2.233 was set manually on the VNA
    ## Netmask 255.255.255.0
    ## Gateway was left blank
    vna = AgilentE5062A("TCPIP::192.168.2.233::inst0::INSTR")


    ## Use Channel 1
    ch = vna.channels[1]

    ch.visible_traces = 1

    for i, (tr, parameter) in enumerate(zip(ch.traces.values(), ['S21'])):
        tr.parameter = parameter

    ch.averages = 1
    ch.averaging_enables = True
    ch.trigger_continuous = False
    vna.trigger_source = 'BUS'
    vna.abort()
    ch.restart_averaging()
    ch.IF_bandwidth = 100
    ch.display_layout = 'D1'

    ch.start_frequency = fl
    ch.stop_frequency = fu
    for _ in range(ch.averages):
        ch.trigger_initiate()
        vna.trigger_single()
        vna.wait_for_complete()
        #ch.display_layout(D1)

    freqs = ch.frequencies
    s_matrix = np.empty((freqs.size,1))
    for i, tr in enumerate(ch.traces.values()):
        tr.activate()
        ch.trace_format = 'MLOG'
        re, im = ch.data
        s_matrix = re

    peaks, _ = find_peaks(s_matrix, height=height)

    return freqs[peaks[PeakNum - 1]]

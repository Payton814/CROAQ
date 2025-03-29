#############################################
##
##  Programmer: Payton Linton
##  Program: getQraw.py
##  Purpose: This code, developed for CROAQ, is meant to take in the raw S21 data
##           from the VNA and use the raw data to determine the Q of the resonance
##
##  NOTE: This code assumes that the array of data passed to it only contains 1 resonant peak
##  NOTE: This code assumed that the S21 data is in logmag format
##
##############################################

import numpy as np

def getQraw(f, S21):
    fres = f[S21.argmax()] ## The resonant frequency occurs at the maximum in the data, assuming 1 peak

    ## By definition the S21 in log scale < 0
    ## To use the raw data to get the Q we need to find the -3dB point from resonance.
    ## Easiest way to do this is to set the -3dB point at 0 and find the minimum.
    ## So we take the logmag of S21, offset but value of fres (puts peak at 0)
    ## then offset by 3 (puts -3dB point at 0)
    ## Finally take abs of data. This ensures all values are positive and the points closest to 0 are the -3dB
    S21alt = abs(10*np.log10(S21) + abs(10*np.log10(S21[S21.argmax()])) + 3)

    ## Q is defined as fres/fwhm. Need to get the -3dB point to the right and to the left of fres
    Qfr = f[S21.argmax() + S21alt[S21.argmax():].argmin()]
    Qfl = f[S21alt[:S21.argmax()].argmin()]

    ## fwhm is the difference between -3dB right and -3dB left
    fwhm = Qfr - Qfl
    
    ## Calculate Q
    Q = fres/fwhm

    return Q
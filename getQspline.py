#############################################
##
##  Programmer: Payton Linton
##  Program: getQspline.py
##  Purpose: This code, developed for CROAQ, is meant to take in the raw S21 data
##           from the VNA and interpolate the data to determine the Q of the resonance
##
##  NOTE: This code assumes that the array of data passed to it only contains 1 resonant peak
##  NOTE: This code assumes the S21 data being passed is as normal mag. Meaning the values 
##        are between 0 and 1
##
##############################################

import numpy as np
from scipy.interpolate import UnivariateSpline

def getQspline(f, S21):
    fres = f[S21.argmax()] ## The resonant frequency occurs at the maximum in the data, assuming 1 peak

    ## Q is defined as fres/fwhm. Need to get the -3dB point to the right and to the left of fres

    ## Using the S21 data, transform the data to set the -3dB point at 0
    ## interpolate the data. The roots of this transformed data are the -3dB points
    spline = UnivariateSpline(f, S21-np.max(S21)/2, s=0)
    Qfl, Qfr = spline.roots() # find the roots

    ## fwhm is the difference between -3dB right and -3dB left
    fwhm = abs(Qfr - Qfl)
    
    ## Calculate Q
    Q = fres/fwhm

    return Q

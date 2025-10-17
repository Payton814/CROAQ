import pyvisa
import numpy as np

def getS21(IFBANDWIDTH, fstart, fend, npoints, analyzer = 'OSU'):
    # Connect to VNA
    rm = pyvisa.ResourceManager()
    vna = rm.open_resource(rm.list_resources()[1])  # This grabs resources seen by pyvisa and assumes the desired one is the send one
    print(vna.query("*IDN?"))
    vna.timeout = 90000 ## Timeout of 60sec

    # Reset and configure
    vna.write("*RST")
    vna.write("*CLS")

    # Define S21 measurement
    if (analyzer == 'OSU'):
        vna.write("CALC1:PAR1:DEF S21")
        vna.write("CALC1:PAR1:SEL")
    else:
        vna.write("CALC1:PAR:DEF 'my S21', S21")
        #vna.write("CALC1:PAR1:EXT 'my S21', 'S21'")
        vna.write("DISP:WIND1:TRAC1:DEL")
        vna.write("DISP:WIND1:TRAC1:FEED 'my S21'")
        vna.write("CALC1:PAR1:SEL 'my S21'")


    vna.write(f"SENS1:FREQ:STAR {fstart}")
    vna.write(f"SENS1:FREQ:STOP {fend}")
    vna.write(f"SENS1:SWE:POIN {npoints}")
    vna.write(f"SENS1:BAND {IFBANDWIDTH}")
    # Set format to log magnitude
    vna.write("CALC1:FORM MLOG")
    vna.write("*WAI")
    if (analyzer == 'OSU'):
        vna.write("TRIG:SOUR BUS")
    else:
        vna.write("TRIG:SOUR MAN")
        vna.write("FORM:DATA ASCII")
    #vna.write("CALC1:PAR1:DEF S21")
    #vna.write("CALC1:PAR1:SEL")


    # Trigger sweep and wait for completion
    vna.write("INIT1:IMM")
    #vna.query("*OPC?")
    vna.write("*WAI")
    #vna.write("TRIG:SING")
    vna.query("*OPC?")

    if (analyzer == 'OSU'):
        # Get frequency array
        freq_data = vna.query("SENS1:FREQ:DATA?")
        freq_array = np.fromstring(freq_data, sep=',')
        #print(freq_array)
        # Get S21 log magnitude data
        s21_data = vna.query("CALC1:DATA:FDAT?")
        s21_logmag = np.fromstring(s21_data, sep=',')
        s21_logmag = s21_logmag[::2]
    else:
        freq_array = np.linspace(fstart, fend, npoints)
        s21_data = vna.query("CALC1:DATA? FDATA")
        s21_logmag = np.fromstring(s21_data, sep = ',')
    #print(len(s21_logmag))
    return freq_array, s21_logmag
#plt.plot(freq_array, s21_logmag)
#plt.show()
# Combine and print
#for f, s in zip(freq_array, s21_logmag):
#    print(f"{f:.2f} Hz : {s:.2f} dB")

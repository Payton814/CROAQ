import pyvisa
import numpy as np

def getS21(IP, IFBANDWIDTH, fstart, fend, npoints):
    # Connect to VNA
    rm = pyvisa.ResourceManager()
    vna = rm.open_resource('TCPIP::' + str(IP) + '::INSTR')  # Replace with your VNA's address
    print(vna.query("*IDN?"))
    vna.timeout = 30000

    # Reset and configure
    vna.write("*RST")
    vna.write("*CLS")

    # Define S21 measurement
    vna.write("CALC1:PAR1:DEF S21")
    vna.write("CALC1:PAR1:SEL")


    vna.write(f"SENS1:FREQ:STAR {fstart}")
    vna.write(f"SENS1:FREQ:STOP {fend}")
    vna.write(f"SENS1:SWE:POIN {npoints}")
    vna.write(f"SENS1:BAND {IFBANDWIDTH}")
    # Set format to log magnitude
    vna.write("CALC1:FORM MLOG")
    vna.write("*WAI")
    vna.write("TRIG:SOUR BUS")

    #vna.write("CALC1:PAR1:DEF S21")
    #vna.write("CALC1:PAR1:SEL")


    # Trigger sweep and wait for completion
    vna.write("INIT1:IMM")
    #vna.query("*OPC?")

    vna.write("TRIG:SING")
    vna.query("*OPC?")
    # Get frequency array
    freq_data = vna.query("SENS1:FREQ:DATA?")
    freq_array = np.fromstring(freq_data, sep=',')
    #print(freq_array)
    # Get S21 log magnitude data
    s21_data = vna.query("CALC1:DATA:FDAT?")
    s21_logmag = np.fromstring(s21_data, sep=',')
    s21_logmag = s21_logmag[::2]
    #print(len(s21_logmag))
    return freq_array, s21_logmag
#plt.plot(freq_array, s21_logmag)
#plt.show()
# Combine and print
#for f, s in zip(freq_array, s21_logmag):
#    print(f"{f:.2f} Hz : {s:.2f} dB")

import pyvisa
import numpy as np
import time
import matplotlib.pyplot as plt

# Connect to VNA
rm = pyvisa.ResourceManager()
vna = rm.open_resource('TCPIP::192.168.2.233::INSTR')  # Replace with your VNA's address
print(vna.query("*IDN?"))
vna.timeout = 30000

# Reset and configure
vna.write("*RST")
vna.write("*CLS")

# Define S21 measurement
vna.write("CALC1:PAR1:DEF S21")
vna.write("CALC1:PAR1:SEL")

#vna.write("*WAI")
# Set frequency sweep
start_freq = 1.3e9   # 1 MHz
stop_freq = 1.5e9    # 1 GHz
points = 1601
if_bandwidth = 100

vna.write(f"SENS1:FREQ:STAR {start_freq}")
vna.write(f"SENS1:FREQ:STOP {stop_freq}")
vna.write(f"SENS1:SWE:POIN {points}")
vna.write(f"SENS1:BAND {if_bandwidth}")
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
print(len(s21_logmag))

plt.plot(freq_array, s21_logmag)
plt.show()
# Combine and print
#for f, s in zip(freq_array, s21_logmag):
#    print(f"{f:.2f} Hz : {s:.2f} dB")

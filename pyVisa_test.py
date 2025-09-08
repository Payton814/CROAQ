import pyvisa
import numpy as np

# Connect to VNA
rm = pyvisa.ResourceManager()
vna = rm.open_resource('TCPIP0::192.168.2.233::inst0::INSTR')  # Replace with your VNA's address
vna.timeout = 10000

# Reset and configure
vna.write("*RST")
vna.write("*CLS")

# Define S21 measurement
vna.write("CALC1:PAR:DEF 'Meas1', S21")
vna.write("DISP:WIND1:TRAC1:FEED 'Meas1'")

# Set frequency sweep
start_freq = 1e9   # 1 MHz
stop_freq = 2e9    # 1 GHz
points = 1601

vna.write(f"SENS1:FREQ:STAR {start_freq}")
vna.write(f"SENS1:FREQ:STOP {stop_freq}")
vna.write(f"SENS1:SWE:POIN {points}")

# Set format to log magnitude
vna.write("CALC1:FORM LOGM")

# Trigger sweep and wait for completion
vna.write("INIT1:IMM")
vna.query("*OPC?")

# Get frequency array
freq_data = vna.query("SENS1:FREQ:DATA?")
freq_array = np.fromstring(freq_data, sep=',')

# Get S21 log magnitude data
s21_data = vna.query("CALC1:DATA? FDATA")
s21_logmag = np.fromstring(s21_data, sep=',')

# Combine and print
for f, s in zip(freq_array, s21_logmag):
    print(f"{f:.2f} Hz : {s:.2f} dB")

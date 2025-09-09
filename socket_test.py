import socket
import time
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# User Inputs
# -----------------------------
VNA_IP = "192.168.2.233"  # Replace with your VNA IP
VNA_PORT = 5025

START_FREQ = 1e9           # Hz
STOP_FREQ  = 1.3e9           # Hz
NUM_POINTS = 201
IF_BANDWIDTH = 1e3         # Hz

# -----------------------------
# SCPI helper
# -----------------------------
def send_scpi(sock, cmd, read=False):
    cmd = cmd.strip() + "\n"
    sock.sendall(cmd.encode())
    if read:
        return sock.recv(1000000).decode().strip()
    return None

# -----------------------------
# Main measurement function
# -----------------------------
def measure_s21():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(30)  # generous timeout for slow sweeps
    sock.connect((VNA_IP, VNA_PORT))

    try:
        # Identify instrument
        idn = send_scpi(sock, "*IDN?", True)
        print("Connected to:", idn)

        # Reset and clear
        send_scpi(sock, "*RST")
        send_scpi(sock, "*CLS")

        # Set sweep parameters
        send_scpi(sock, f"SENS1:FREQ:STAR {START_FREQ}")
        send_scpi(sock, f"SENS1:FREQ:STOP {STOP_FREQ}")
        send_scpi(sock, f"SENS1:SWE:POIN {NUM_POINTS}")
        send_scpi(sock, f"SENS1:BAND {IF_BANDWIDTH}")

        send_scpi(sock, "*WAI")
        # **ENA-L specific**: select S21 as active parameter
        send_scpi(sock, "CALC1:PAR1:DEF S21")
        send_scpi(sock, "CALC1:PAR1:SEL")

        send_scpi(sock, "*WAI")
        # SSelect trigger source
        send_scpi(sock, "TRIG:SOUR BUS")

        # Set display format to log magnitude (dB)
        send_scpi(sock, "CALC1:FORM MLOG")
        send_scpi(sock, "*WAI")
        send_scpi(sock, "INIT1:IMM")
        send_scpi(sock, "*WAI")
        send_scpi(sock, "*TRG")

        send_scpi(sock, "*WAI")

        # Retrieve data
        send_scpi(sock, "FORM:DATA ASCii")
        send_scpi(sock, "*OPC?", read = True)
        data_str = send_scpi(sock, "CALC1:DATA:FDAT?", True)
        print(data_str)
        logmag = np.array([float(x) for x in data_str.split(",")])
        #print(logmag)
        # Frequency axis
        freqs = np.linspace(START_FREQ, STOP_FREQ, NUM_POINTS)

        # Return list of (frequency, S21_dB) tuples
        return list((freqs, logmag))
        #return 0

    finally:
        sock.close()
        print("Connection closed.")

# -----------------------------
# Run example
# -----------------------------
if __name__ == "__main__":
    s21_data = measure_s21()
    #plt.plot(s21_data[0], s21_data[1])
    #plt.show()
    #for f, db in s21_data[:5]:
    #    print(f"{f/1e9:.3f} GHz : {db:.2f} dB")

import socket
import time
import numpy as np

# -----------------------------
# User Inputs
# -----------------------------
VNA_IP = "192.168.2.233"  # Replace with your VNA IP
VNA_PORT = 5025

START_FREQ = 1e9          # Hz
STOP_FREQ  = 2e9          # Hz
NUM_POINTS = 1601
IF_BANDWIDTH = 1e3        # Hz

# -----------------------------
# SCPI Helper
# -----------------------------
def send_scpi(sock, cmd, read=False):
    cmd = cmd.strip() + "\n"
    sock.sendall(cmd.encode())
    if read:
        return sock.recv(1000000).decode().strip()
    return None

# -----------------------------
# Check if sweep is complete
# -----------------------------
def wait_sweep_complete(sock, timeout=30):
    """
    Polls the VNA until the sweep is complete.
    Uses *OPC? query which returns '1' when operations complete.
    """
    start_time = time.time()
    while True:
        try:
            resp = send_scpi(sock, "*OPC?", True)
            if resp.strip() == '1':
                return True
        except socket.timeout:
            pass
        if time.time() - start_time > timeout:
            raise TimeoutError("Sweep did not complete in time")
        time.sleep(0.1)

# -----------------------------
# Main Measurement Function
# -----------------------------
def measure_s21():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(30)  # long timeout for slow sweeps
    sock.connect((VNA_IP, VNA_PORT))

    try:
        print("Connected. Instrument ID:", send_scpi(sock, "*IDN?", True))

        # Reset and clear
        send_scpi(sock, "*RST")
        send_scpi(sock, "*CLS")

        # Sweep settings
        send_scpi(sock, f"SENS1:FREQ:STAR {START_FREQ}")
        send_scpi(sock, f"SENS1:FREQ:STOP {STOP_FREQ}")
        send_scpi(sock, f"SENS1:SWE:POIN {NUM_POINTS}")
        send_scpi(sock, f"SENS1:BAND {IF_BANDWIDTH}")

        # Assign S21 directly to trace 1
        send_scpi(sock, "DISP:WIND1:TRAC1:FEED S21")

        # Set display format to log magnitude
        send_scpi(sock, "CALC1:FORM MLOG")

        # Trigger sweep
        send_scpi(sock, "INIT1:IMM; *WAI")

        # Wait until sweep finishes
        #wait_sweep_complete(sock, timeout=30)

        # Fetch data
        data_str = send_scpi(sock, "CALC1:DATA? FDATA", True)
        logmag = np.array([float(x) for x in data_str.split(",")])

        # Frequency axis
        freqs = np.linspace(START_FREQ, STOP_FREQ, NUM_POINTS)

        return list(zip(freqs, logmag))

    finally:
        sock.close()
        print("Connection closed.")

# -----------------------------
# Run Example
# -----------------------------
if __name__ == "__main__":
    s21_data = measure_s21()
    for f, db in s21_data[:5]:
        print(f"{f/1e9:.3f} GHz : {db:.2f} dB")

import socket
import numpy as np

IP = "192.168.2.233" ## IP address for the network analyzer in Beatty lab
IF_BANDWIDTH = 100 ## In Hz
PORT = 5025
NUM_POINTS = 1601 ## Number of points the VNA will take in the given window
                  ## E5062A is capable of up to 1601 points
START_FREQ = 1e9
STOP_FREQ = 3e9

def send_scpi(sock, command, read_response=False):
    """Send SCPI command, optionally read response."""
    cmd = command.strip() + "\n"
    sock.sendall(cmd.encode())

    if read_response:
        response = sock.recv(1000000).decode().strip()
        return response
    return None

def measure_s21_logmag():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)

    try:
        print(f"Connecting to VNA at {IP}:{PORT}...")
        sock.connect((IP, PORT))
        print("Connected!")

        # Identify instrument
        idn = send_scpi(sock, "*IDN?", True)
        print("Instrument:", idn)

        # Reset instrument (optional)
        send_scpi(sock, "*RST")
        send_scpi(sock, "*CLS")

        # Configure sweep parameters
        send_scpi(sock, f"SENS1:FREQ:START {START_FREQ}")
        send_scpi(sock, f"SENS1:FREQ:STOP {STOP_FREQ}")
        send_scpi(sock, f"SENS1:SWE:POIN {NUM_POINTS}")
        send_scpi(sock, f"SENS1:BAND {IF_BANDWIDTH}")

        # Define and select S21
        send_scpi(sock, "CALC1:PAR:DEF 'Meas1', S21")
        send_scpi(sock, "CALC1:PAR:SEL 'Meas1'")

        # Set display format to log magnitude (dB)
        send_scpi(sock, "CALC1:FORM MLOG")

        # Trigger sweep and wait
        send_scpi(sock, "INIT1:IMM; *WAI")

        # Ensure ASCII output
        send_scpi(sock, "FORM:DATA ASC")

        # Get frequency axis from instrument
        f_start = float(send_scpi(sock, "SENS1:FREQ:START?", True))
        f_stop  = float(send_scpi(sock, "SENS1:FREQ:STOP?", True))
        npts    = int(send_scpi(sock, "SENS1:SWE:POIN?", True))

        freqs = np.linspace(f_start, f_stop, npts)

        # Fetch log-magnitude data
        data = send_scpi(sock, "CALC1:DATA? FDATA", True)
        logmag = np.array([float(x) for x in data.split(",")])

        if len(logmag) != npts:
            print(f"Warning: expected {npts} points, got {len(logmag)}")

        # Combine into list of (freq, dB)
        result = list(zip(freqs, logmag))

        print(f"Retrieved {len(result)} points.")
        return result

    except socket.error as e:
        print("Socket error:", e)
        return None

    finally:
        sock.close()
        print("Connection closed.")

# -----------------------------
# Run example
# -----------------------------
if __name__ == "__main__":
    s21_data = measure_s21_logmag()
    if s21_data:
        # Show first 5 points
        for f, db in s21_data[:5]:
            print(f"{f/1e9:.3f} GHz : {db:.2f} dB")
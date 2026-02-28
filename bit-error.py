import socket
import numpy as np
import time
import sys
import select

# --- CONFIGURATION ---
TCP_IP = '127.0.0.1' 
TCP_PORT = 14423
BUFFER_SIZE = 1024 * 256 

def run_raw_radar():
    # Initial sensitivity multiplier
    multiplier = 2.5
    
    print("--- Binary Shadow Radar (Live Adjust) ---")
    print(f"Connecting to: {TCP_IP}:{TCP_PORT}")
    print("Commands: [+] Increase Sens [-] Decrease Sens")
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((TCP_IP, TCP_PORT))
        print("Connected! Calibrating...")

        # Calibration Phase
        time.sleep(1)
        data = s.recv(BUFFER_SIZE)
        samples = np.frombuffer(data, dtype=np.uint8).astype(np.float32) - 127.5
        baseline = np.var(samples**2)
        print(f"Calibration Done. Baseline: {baseline:.2e}")

        while True:
            # 1. Non-blocking keyboard check for sensitivity adjustment
            if select.select([sys.stdin], [], [], 0)[0]:
                cmd = sys.stdin.read(1)
                if cmd == '+':
                    multiplier += 0.2
                    print(f"[*] Sensitivity lowered (Multi: {multiplier:.1f})")
                elif cmd == '-':
                    multiplier -= 0.2
                    multiplier = max(1.1, multiplier)
                    print(f"[*] Sensitivity raised (Multi: {multiplier:.1f})")

            # 2. Process Signal Data
            data = s.recv(BUFFER_SIZE)
            if not data: break
            
            samples = np.frombuffer(data, dtype=np.uint8).astype(np.float32) - 127.5
            current_var = np.var(samples**2)
            
            # 3. Detection Trigger
            if current_var > (baseline * multiplier):
                print(f"[!] Binary Shadow Detected: {time.strftime('%H:%M:%S')}")
            
            time.sleep(0.05)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    run_raw_radar()

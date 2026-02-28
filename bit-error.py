import socket
import numpy as np
import time
import sys
import select

# --- CONFIGURATION ---
TCP_IP = '127.0.0.1' 
TCP_PORT = 14423
BUFFER_SIZE = 1024 * 256 

def get_snapshot(s):
    """Captures a raw moment of the airwaves."""
    data = s.recv(BUFFER_SIZE)
    # Convert raw bytes to IQ signal power
    samples = np.frombuffer(data, dtype=np.uint8).astype(np.float32) - 127.5
    return np.var(samples**2)

def run_raw_radar():
    multiplier = 1.2  # Start very sensitive
    history = []
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((TCP_IP, TCP_PORT))
        
        print("Connecting to RTL-SDR Driver...")
        time.sleep(1)
        baseline = get_snapshot(s)
        
        print(f"--- Radar Online (Dededo Node) ---")
        print(f"Baseline: {baseline:.2e} | Sens: {multiplier}x")
        print("Keys: [r] Recalibrate | [+] / [-] Sensitivity")

        while True:
            # 1. Live Input Logic
            if select.select([sys.stdin], [], [], 0)[0]:
                cmd = sys.stdin.read(1)
                if cmd == 'r':
                    baseline = get_snapshot(s)
                    print(f"[*] Recalibrated Baseline: {baseline:.2e}")
                elif cmd == '+': multiplier += 0.2
                elif cmd == '-': multiplier = max(1.05, multiplier - 0.2)
                print(f"[*] Multiplier set to {multiplier:.2f}x")

            # 2. Capture and Analyze the 'Trace'
            current_var = get_snapshot(s)
            
            # Smoothing the signal (Moving Average of 4)
            history.append(current_var)
            if len(history) > 4: history.pop(0)
            smoothed_var = np.mean(history)
            
            # 3. Detection Trigger
            # If the current jitter is higher than the baseline * multiplier
            if smoothed_var > (baseline * multiplier):
                diff = (smoothed_var / baseline)
                print(f"[!] PHYSICAL TRACE: {time.strftime('%H:%M:%S')} | Intensity: {diff:.2f}x")
            
            time.sleep(0.05)

    except Exception as e:
        print(f"Connection Lost: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    run_raw_radar()

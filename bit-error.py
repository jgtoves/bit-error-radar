import socket
import numpy as np
import time
import sys
import select

# --- CONFIGURATION ---
TCP_IP = '127.0.0.1' 
TCP_PORT = 14423
BUFFER_SIZE = 1024 * 256 

def calibrate(s):
    print("Calibrating... Stay still.")
    time.sleep(1)
    data = s.recv(BUFFER_SIZE)
    samples = np.frombuffer(data, dtype=np.uint8).astype(np.float32) - 127.5
    return np.var(samples**2)

def run_raw_radar():
    multiplier = 1.5 # Lowered for easier detection
    history = []
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((TCP_IP, TCP_PORT))
        
        baseline = calibrate(s)
        print(f"Online. Baseline: {baseline:.2e} | Multiplier: {multiplier}")
        print("Keys: [r] Reset Calibration | [+] / [-] Sensitivity")

        while True:
            # 1. Input Handling
            if select.select([sys.stdin], [], [], 0)[0]:
                cmd = sys.stdin.read(1)
                if cmd == 'r':
                    baseline = calibrate(s)
                    print(f"[*] Calibration Reset. New Baseline: {baseline:.2e}")
                elif cmd == '+': multiplier += 0.5
                elif cmd == '-': multiplier = max(1.1, multiplier - 0.5)

            # 2. Signal Processing
            data = s.recv(BUFFER_SIZE)
            if not data: break
            
            samples = np.frombuffer(data, dtype=np.uint8).astype(np.float32) - 127.5
            current_var = np.var(samples**2)
            
            # Simple Smoothing
            history.append(current_var)
            if len(history) > 5: history.pop(0)
            avg_var = np.mean(history)
            
            # 3. Detection
            if avg_var > (baseline * multiplier):
                print(f"[!] TRACE DETECTED: {time.strftime('%H:%M:%S')} | Jump: {avg_var/baseline:.1f}x")
            
            time.sleep(0.05)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    run_raw_radar()

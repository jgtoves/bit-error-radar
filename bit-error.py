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
    multiplier = 1.3  # Start low for testing
    baseline_history = []
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((TCP_IP, TCP_PORT))
        print("Connected to RTL-SDR Bridge...")

        while True:
            # 1. Capture the Raw Trace
            data = s.recv(BUFFER_SIZE)
            if not data: break
            
            samples = np.frombuffer(data, dtype=np.uint8).astype(np.float32) - 127.5
            current_var = np.var(samples**2)
            
            # 2. Rolling Baseline (The "Memory" of the room)
            baseline_history.append(current_var)
            if len(baseline_history) > 50: baseline_history.pop(0)
            current_baseline = np.median(baseline_history)
            
            # 3. Calculate "Shadow Intensity"
            intensity = current_var / current_baseline if current_baseline > 0 else 1.0
            
            # 4. Feedback Logic
            # This line lets you see the 'jitter' in real-time
            sys.stdout.write(f"\rIntensity: {intensity:.2f}x | Multiplier: {multiplier:.1f}  ")
            sys.stdout.flush()

            if intensity > multiplier:
                print(f"\n[!] MOVEMENT DETECTED: {time.strftime('%H:%M:%S')}")
            
            # 5. Live Controls
            if select.select([sys.stdin], [], [], 0)[0]:
                cmd = sys.stdin.read(1)
                if cmd == '+': multiplier += 0.1
                elif cmd == '-': multiplier = max(1.1, multiplier - 0.1)

            time.sleep(0.05)

    except Exception as e:
        print(f"\nRadar Glitch: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    run_raw_radar()

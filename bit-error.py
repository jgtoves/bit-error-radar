import socket
import numpy as np
import time
import sys

# --- CONFIGURATION ---
# These must match exactly what is shown in your RTL-SDR Driver APK
TCP_IP = '127.0.0.1' 
TCP_PORT = 14423
BUFFER_SIZE = 1024 * 256 

def run_raw_radar():
    print("--- Binary Shadow Radar Initializing ---")
    print(f"Connecting to: {TCP_IP}:{TCP_PORT}")
    
    try:
        # Create the socket connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5) # Don't hang forever if the APK isn't running
        s.connect((TCP_IP, TCP_PORT))
        print("Connected! Starting calibration...")

        # 1. CALIBRATION PHASE
        # We capture the baseline 'noise' of your room in Dededo.
        # Stay still for 2 seconds while this happens.
        time.sleep(1)
        data = s.recv(BUFFER_SIZE)
        if not data:
            print("Error: No data received from driver.")
            return

        # Convert raw bytes to signal power
        samples = np.frombuffer(data, dtype=np.uint8).astype(np.float32) - 127.5
        baseline_variance = np.var(samples**2)
        
        # 2. SENSITIVITY THRESHOLD
        # 2.5 is a good start. Increase to 3.0 if you get false alarms.
        threshold = baseline_variance * 2.5 
        print(f"Calibration Complete.")
        print(f"Baseline Noise: {baseline_variance:.2e}")
        print(f"Detection Threshold: {threshold:.2e}")
        print("Monitoring for physical traces... (Ctrl+C to stop)")

        # 3. MAIN MONITORING LOOP
        while True:
            data = s.recv(BUFFER_SIZE)
            if not data:
                break
            
            # Process the current chunk of 'air'
            samples = np.frombuffer(data, dtype=np.uint8).astype(np.float32) - 127.5
            current_variance = np.var(samples**2)
            
            # Compare current 'jitter' against the baseline
            if current_variance > threshold:
                timestamp = time.strftime('%H:%M:%S')
                print(f"[!] Binary Shadow Detected at {timestamp}")
            
            # Small pause to keep the CPU from redlining
            time.sleep(0.05)

    except socket.timeout:
        print("Error: Connection timed out. Is the APK Driver started?")
    except KeyboardInterrupt:
        print("\nRadar offline. User requested stop.")
    except Exception as e:
        print(f"Unexpected Glitch: {e}")
    finally:
        s.close()
        print("Socket closed.")

if __name__ == "__main__":
    run_raw_radar()

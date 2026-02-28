import os
import socket
import numpy as np
import time

# Coordination for the RTL-SDR Driver APK
TCP_IP = '127.0.0.1' 
TCP_PORT = 14423
BUFFER_SIZE = 1024 * 256 

def run_raw_radar():
    print(f"Connecting to Raw Trace at {TCP_IP}:{TCP_PORT}...")
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        print("Connected. Calibrating the room's noise floor...")

        # 1. Calibration: Capturing the 'empty' state of the room
        time.sleep(1)
        data = s.recv(BUFFER_SIZE)
        samples = np.frombuffer(data, dtype=np.uint8).astype(np.float32) - 127.5
        baseline = np.var(samples**2)
        # 2. Sensitivity: Adjust the multiplier (2.5) if it's too twitchy
        threshold = baseline * 2.5 
        print(f"Calibration Complete. Noise Floor: {baseline:.2e}")

        while True:
            data = s.recv(BUFFER_SIZE)
            if not data:
                break
            
            # 3. Process the 'Binary Shadow'
            samples = np.frombuffer(data, dtype=np.uint8).astype(np.float32) - 127.5
            current_var = np.var(samples**2)
            
            # 4. Detection Event
            if current_var > threshold:
                print(f"[!] Binary Shadow Detected: {time.strftime('%H:%M:%S')}")
            
            # Keep this line exactly aligned with the 'if' block above
            time.sleep(0.05)

    except Exception as e:
        print(f"Trace Interrupted: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    run_raw_radar()
    
            time.sleep(0.05)

    except Exception as e:
        print(f"Trace Interrupted: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    run_raw_radar()
    except Exception as e:
        print(f"Logic Error: {e}")
    finally:
        try: client.close()
        except: pass

if __name__ == "__main__":
    run_radar()

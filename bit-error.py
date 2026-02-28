import os
import socket
import numpy as np
import time

# 1. Match the coordinates you found in the APK
TCP_IP = '127.0.0.1' 
TCP_PORT = 14423
BUFFER_SIZE = 1024 * 256 # Capture large 'shadows'

def run_raw_radar():
    print(f"Connecting to Raw Trace at {TCP_IP}:{TCP_PORT}...")
    
    try:
        # Create a raw socket to talk to the APK
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        print("Connected. Recording the instability of the room...")

        # Calibration
        time.sleep(1)
        data = s.recv(BUFFER_SIZE)
        # Convert binary bytes into numbers (IQ samples)
        samples = np.frombuffer(data, dtype=np.uint8).astype(np.float32) - 127.5
        baseline = np.var(samples**2)
        threshold = baseline * 2.5
        print(f"Calibration Complete. Noise Floor: {baseline:.2e}")

        while True:
            data = s.recv(BUFFER_SIZE)
            if not data: break
            
            samples = np.frombuffer(data, dtype=np.uint8).astype(np.float32) - 127.5
            current_var = np.var(samples**2)
            
            if current_var > threshold:
                print(f"[!] Binary Shadow Detected: {time.strftime('%H:%M:%S')}")
            
            time.sleep(0.05)

    except Exception as e:
        print(f"Trace Interrupted: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    run_raw_radar()                print(f"[!] Binary Shadow Detected: {time.strftime('%H:%M:%S')}")
            
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

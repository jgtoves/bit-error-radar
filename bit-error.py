import os
import socket
import numpy as np
import time

# Use the coordinates from your APK
TCP_IP = '127.0.0.1' 
TCP_PORT = 14423
BUFFER_SIZE = 1024 * 256 

def run_raw_radar():
    print(f"Connecting to Raw Trace at {TCP_IP}:{TCP_PORT}...")
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        print("Connected. Calibrating the room's noise floor...")

        # Initial calibration to sense the 'empty' room
        time.sleep(1)
        data = s.recv(BUFFER_SIZE)
        samples = np.frombuffer(data, dtype=np.uint8).astype(np.float32) - 127.5
        baseline = np.var(samples**2)
        threshold = baseline * 2.5 
        print(f"Calibration Complete. Noise Floor: {baseline:.2e}")

        while True:
            data = s.recv(BUFFER_SIZE)
            if not data: break
            
            # Convert the raw bytes into a signal 'power' value
            samples = np.frombuffer(data, dtype=np.uint8).astype(np.float32) - 127.5
            current_var = np.var(samples**2)
            
            # If the room 'jitters' more than the baseline, a person is detected
            if current_var > threshold:
                print(f"[!] Binary Shadow Detected: {time.strftime('%H:%M:%S')}")
            
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

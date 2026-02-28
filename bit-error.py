import os
import numpy as np
import time

# Essential for Termux environment
os.environ['RTLSDR_CLIENT_MODE'] = 'true'
from rtlsdr import RtlSdrTcpClient

def run_radar():
    try:
        # Match this exactly to what your APK shows
        # Use 127.0.0.1 if the APK is on the SAME phone
        print("Connecting to RTL-SDR Driver on 127.0.0.1:14423...")
        client = RtlSdrTcpClient(hostname='127.0.0.1', port=14423)
        
        # Give the connection a moment to stabilize
        time.sleep(2)

        # Tune to the 5G frequency 'trace'
        client.center_freq = 710e6  
        client.sample_rate = 2.048e6
        client.gain = 'auto'

        print("Radar Online. Monitoring for binary shadows...")
        
        while True:
            # Read raw samples from the TCP bridge
            samples = client.read_samples(1024*256)
            # Calculate the variance (the jitter of the physical world)
            instability = np.var(np.abs(samples)**2)
            
            # If the instability spikes, someone is in the room
            if instability > 1.5e-06: # Adjust this value based on your room's 'quiet' level
                print(f"[!] Presence Detected at {time.strftime('%H:%M:%S')}")
            
            time.sleep(0.1)

    except Exception as e:
        print(f"Logic Error: {e}")
    finally:
        try: client.close()
        except: pass

if __name__ == "__main__":
    run_radar()

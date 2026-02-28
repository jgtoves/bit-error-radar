import os
import numpy as np
import time

# Keep this to bypass the missing C libraries
os.environ['RTLSDR_CLIENT_MODE'] = 'true'
from rtlsdr import RtlSdrTcpClient

def run_radar():
    try:
        # 1. Connect to the APK Driver
        print("Connecting to RTL-SDR Driver APK...")
        client = RtlSdrTcpClient(hostname='0.0.0.0', port=14423)
        
        # Give the socket a second to breathe
        time.sleep(1)

        # 2. Configure for Guam 5G (Docomo/IT&E 700MHz range)
        print("Tuning to 710MHz...")
        client.center_freq = 710e6  
        client.sample_rate = 2.048e6
        client.gain = 'auto'

        print("Radar Online: Calibrating...")
        
        # Capture initial samples to set the baseline
        samples = client.read_samples(1024*256)
        baseline_var = np.var(np.abs(samples)**2)
        threshold = baseline_var * 2.2 # Sensitivity multiplier

        while True:
            samples = client.read_samples(1024*256)
            current_var = np.var(np.abs(samples)**2)
            
            if current_var > threshold:
                print(f"[!] Binary Trace Detected: {time.strftime('%H:%M:%S')}")
            
            time.sleep(0.1)

    except Exception as e:
        print(f"Connection Glitch: {e}")
        print("Make sure the RTL-SDR Driver APK is 'Started' and showing 'Listening'.")
    finally:
        try: client.close()
        except: pass

if __name__ == "__main__":
    run_radar()

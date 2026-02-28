import os
import numpy as np
import time

# Essential: Force pyrtlsdr to skip looking for local C libraries 
# and use the TCP Client mode instead.
os.environ['RTLSDR_CLIENT_MODE'] = 'true'
from rtlsdr import RtlSdrTcpClient

# 1. Connect to the APK Driver (Localhost on port 1234)
client = RtlSdrTcpClient(hostname='127.0.0.1', port=1234)

# 2. Configure for Guam 5G/LTE (IT&E Band 12 or Docomo Band 17)
# Tuning to ~710 MHz captures the 700MHz 'long range' cellular band.
client.center_freq = 710e6  
client.sample_rate = 2.048e6
client.gain = 'auto'

def get_binary_instability():
    samples = client.read_samples(1024*256)
    # Measure the variance of the signal power (the 'jitter')
    power = np.abs(samples)**2
    return np.var(power)

print("Radar Online: Calibrating room noise in Dededo...")
baseline = [get_binary_instability() for _ in range(20)]
threshold = np.mean(baseline) * 2.5 # Adjust multiplier for sensitivity

try:
    while True:
        instability = get_binary_instability()
        if instability > threshold:
            print(f"[!] Binary Trace Detected: Physical Movement at {time.strftime('%H:%M:%S')}")
        time.sleep(0.1)
except KeyboardInterrupt:
    client.close()

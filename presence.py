import numpy as np
from rtlsdr import RtlSdr

# Initialize SDR for a local 5G band (e.g., 700MHz)
sdr = RtlSdr()
sdr.sample_rate = 2.4e6
sdr.center_freq = 700e6  
sdr.gain = 'auto'

def get_signal_variance():
    samples = sdr.read_samples(256*1024)
    # Convert samples to power and measure 'instability'
    power = np.abs(samples)**2
    return np.var(power)

# Establish a baseline for a 'quiet' room in Dededo
baseline = [get_signal_variance() for _ in range(30)]
threshold = np.mean(baseline) + (np.std(baseline) * 3)

print("Monitoring for physical traces in the 5G field...")

try:
    while True:
        v = get_signal_variance()
        if v > threshold:
            print(f"[!] Trace Detected: Physical interference at {v:.2e}")
except KeyboardInterrupt:
    sdr.close()

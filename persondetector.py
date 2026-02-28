import numpy as np
from rtlsdr import RtlSdr

sdr = RtlSdr()
sdr.sample_rate = 2.4e6
sdr.center_freq = 700e6  # Adjust for your strongest local 5G/LTE tower
sdr.gain = 'auto'

def get_signal_variance():
    samples = sdr.read_samples(256*1024)
    # Convert to power and measure how 'unstable' the signal is
    power = np.abs(samples)**2
    return np.var(power)

# Establish a baseline of 'quiet' room noise
baseline = [get_signal_variance() for _ in range(30)]
threshold = np.mean(baseline) + (np.std(baseline) * 3)

print("Monitoring the void for physical traces...")

try:
    while True:
        v = get_signal_variance()
        if v > threshold:
            print("[!] Physical Trace Detected: The field has been breached.")
except KeyboardInterrupt:
    sdr.close()

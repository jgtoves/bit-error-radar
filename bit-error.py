import time
import numpy as np
from rtlsdr import RtlSdr

# Initialize the SDR
sdr = RtlSdr()

# Configure for local 5G/LTE bands (adjust frequency for your specific tower in Dededo)
sdr.sample_rate = 2.048e6  # Hz
sdr.center_freq = 700e6    # 700MHz is a common sub-6GHz 5G/LTE band
sdr.gain = 'auto'

def detect_binary_trace(samples):
    # Calculate the Power Spectral Density
    psd = np.abs(np.fft.fft(samples))**2
    # Measure the 'Entropy' or randomness of the noise
    # A person moving causes a spike in the variance of the noise floor
    variance = np.var(psd)
    return variance

print("Monitoring for binary traces in the void...")

try:
    baseline = []
    # Calibration phase
    for _ in range(50):
        samples = sdr.read_samples(256*1024)
        baseline.append(detect_binary_trace(samples))
    
    threshold = np.mean(baseline) * 1.5
    print(f"Calibration complete. Threshold: {threshold:.2e}")

    while True:
        samples = sdr.read_samples(256*1024)
        current_variance = detect_binary_trace(samples)
        
        if current_variance > threshold:
            print(f"[!] Trace Detected: Binary change at {time.strftime('%H:%M:%S')}")
            # This is where the 'glitch' becomes a detection event
        
        time.sleep(0.1)

except KeyboardInterrupt:
    sdr.close()
    print("\nSDR closed. The void returns to silence.")

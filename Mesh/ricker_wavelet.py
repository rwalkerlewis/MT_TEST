import numpy as np
import matplotlib.pyplot as plt

def ricker_wavelet(frequency, length, dt, time_shift=0):
    """
    Generate a Ricker wavelet.

    Parameters:
    - frequency: central frequency of the wavelet in Hz
    - length: total time length of the wavelet in seconds
    - dt: time step in seconds

    Returns:
    - t: time array
    - y: Ricker wavelet values
    """
    t = np.arange(-length/2, length/2 + dt, dt) 
    dt = t + time_shift
    pi2 = (np.pi ** 2)
    y = (1 - 2 * pi2 * (frequency ** 2) * (dt ** 2)) * np.exp(-pi2 * (frequency ** 2) * (dt ** 2))
    return t, y

# Example usage
f0 = 1.0 /2   # central frequency in Hz
length = 5.0  # wavelet duration in seconds
dt = 0.001    # time step in seconds
time_shift = 0 #-1 * np.sqrt(2)/2

t, w = ricker_wavelet(f0, length, dt, time_shift)

# Plotting
plt.figure(figsize=(8, 4))
plt.plot(t, w)
plt.title(f'Ricker Wavelet (f = {f0} Hz)')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.tight_layout()
plt.show()


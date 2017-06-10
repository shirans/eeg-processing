import numpy as np
# import neo
import matplotlib.pyplot as plt
import mne


print(__doc__)

sfreq = 10000  # Sampling frequency
times = np.arange(0, 100, 0.001)  # Use 10000 samples (10s)

sin = np.sin(times * 10)  # Multiplied by 10 for shorter cycles
cos = np.cos(times * 10)
sinX2 = sin * 2
cosX2 = cos * 2

# Numpy array of size 4 X 10000.
data = np.array([sin, cos, sinX2, cosX2])

# Definition of channel types and names.
ch_types = ['mag', 'mag', 'eeg', 'eeg']
ch_names = ['sin', 'cos', 'sinX2', 'cosX2']

info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)

raw = mne.io.RawArray(data, info)

# Scaling of the figure.
# For actual EEG/MEG data different scaling factors should be used.
scalings = {'mag': 2, 'eeg': 2}


even_id = {'audit:':1,'visual':3}
events = mne.read_events()
raw.plot(n_channels=4, scalings=scalings, title='Data from arrays', show=True, block=False)
# raw.plot(n_channels=4, title='Data from arrays', show=True, block=True)

print("a")

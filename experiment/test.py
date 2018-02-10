import datetime
import random

import matplotlib.pyplot as plt


def create_visual():
    from psychopy import visual, core
    win = visual.Window([400, 400])
    message = visual.TextStim(win, text='hello')
    message.setAutoDraw(True)  # automatically draw every frame
    win.flip()
    core.wait(2.0)
    message.setText('world')  # change properties of existing stim
    win.flip()
    core.wait(2.0)


import numpy as np
import mne

from load_csv import raw_from_path, raw_from_df, concatenate_df, plot_raw_data, plot_events_on_time_ax

#
def example_plot():
    sfreq = 1000  # Sampling frequency
    times = np.arange(0, 10, 0.001)  # Use 10000 samples (10s)

    sin = np.sin(times * 10)  # Multiplied by 10 for shorter cycles
    cos = np.cos(times * 10)
    sinX2 = sin * 2
    cosX2 = cos * 2

    # Numpy array of size 4 X 10000.
    data = np.array([sin, cos, sinX2, cosX2])

    # Definition of channel types and names.
    ch_types = ['mag', 'mag', 'grad', 'grad']
    ch_names = ['sin', 'cos', 'sinX2', 'cosX2']

    info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)

    raw = mne.io.RawArray(data, info)
    scalings = {'mag': 2, 'grad': 2}
    #Scaling of the figure.
    raw.plot(n_channels=4, scalings=scalings, title='Data from arrays',
             show=True, block=True)

# example_plot()
# path = '/Users/shiran/workspace/eeg-processing/raw-data/p300//02-10-18_13-18-21.csv'
path = '/Users/shiran/workspace/eeg-processing/raw-data/p300/02-10-18_12-06-13.csv'
# plot_events_on_time_ax(path)
df = concatenate_df(path)

events = df[['timesamps', 'Stim']].values
# time_s = df['timesamps'].values
# time_s = map(lambda x: datetime.datetime.utcfromtimestamp(x / 1000), time_s)
stim = df['Stim'].values
event_value = []
event_index = []
# y = np.zeros(len(time_s))
for i, event in enumerate(stim):
    if event > 0:
        event_index.append(i)
        event_value.append(event)
        # y[i] = event
events = np.column_stack((event_index, np.zeros(len(event_value)), event_value))
raw = raw_from_path(path)
plot_raw_data(raw, events)

import datetime
import random
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr


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

from load_csv import raw_from_path, raw_from_df, concatenate_df, plot_raw_data, plot_events_on_time_ax, CHANNELS_NAMES, \
    CHANNELS_TYPES


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
    # Scaling of the figure.
    raw.plot(n_channels=4, scalings=scalings, title='Data from arrays',
             show=True, block=True)


def plot_with_events(df, ch_col_name=CHANNELS_NAMES, ch_col_types=CHANNELS_TYPES):
    stim = df['Stim'].values
    event_value = []
    event_index = []
    for i, event in enumerate(stim):
        if event > 0:
            event_index.append(i)
            event_value.append(event)
    events = np.column_stack((event_index, np.zeros(len(event_value)), event_value))
    raw = raw_from_df(df, ch_col_names=ch_col_name, ch_col_types=ch_col_types)
    plot_raw_data(raw, events)
    raw.plot_psd(tmax=np.inf)


def find_corr():
    path = '/Users/shiran/workspace/eeg-processing/raw-data/p300/02-10-18_22-45-45.*'
    df = concatenate_df(path)
    timestamp = df['timestamps'].values
    stim_pos = df[df['Stim'] > 0][['Stim', "timestamps"]]
    new_col = np.zeros(df.shape[0])
    for index, row in stim_pos.iterrows():
        t = row['timestamps']
        s = row['Stim']
        diff = np.abs(timestamp - t)
        ser = np.abs(df['timestamps'] - t) < 500
        indexes = ser[ser == True].index.values
        new_col[min(indexes):max(indexes)] = s
        new_col[indexes] = s
    stimsA = df['StimA'].values
    stims = df['Stim'].values

    for name, values in df.iteritems():
        if name in ['AF7', 'AF8', 'TP9', 'TP10']:
            coff, p_value = pearsonr(values, stims)
            coff_a, p_value_a = pearsonr(values, stimsA)
            print "for column {}, stims: corr= {} p = {}, stimsA: corr={},p={}".format(name, coff, p_value, coff_a,
                                                                                       p_value_a)
    print(df.corr())

from glob import glob

import datetime
import pandas as pd
# from mne import create_info, concatenate_raws
# from mne.channels import read_montage
# from mne.io import RawArray
import mne
import matplotlib.pyplot as plt

import numpy as np

CHANNELS_NAMES = ['TP9', 'AF7', 'AF8', 'TP10', 'Stim']
CHANNELS_TYPES = ['eeg'] * 4 + ['stim']
montage = mne.channels.read_montage('standard_1020')


# montage = mne.channels.read_montage('standard_1005')

def plot_events_on_time_ax(path):
    df = concatenate_df(path)
    time_s = df['timestamps'].values
    time_s = map(lambda x: datetime.datetime.utcfromtimestamp(x / 1000), time_s)
    stim = df['Stim'].values
    event_value = []
    event_index = []
    y = np.zeros(len(time_s))
    for i, event in enumerate(stim):
        if event > 0:
            event_index.append(i)
            event_value.append(event)
            y[i] = event
    plt.plot(time_s, y)
    # beautify the x-labels
    plt.gcf().autofmt_xdate()
    plt.show()


def raw_from_path(path):
    raw_data = []
    files = glob(path)
    for file in files:
        data = pd.read_csv(file, index_col=False)
        raw_data.append(raw_from_df(data))
    return mne.concatenate_raws(raw_data)


def raw_from_df(data, sfreq=256, ch_col_names=CHANNELS_NAMES, ch_col_types=CHANNELS_TYPES):
    print("event distribution:\n{}".format(data.Stim.value_counts()))
    print ("num seconds: %f" % ((data['timestamps'][len(data['timestamps']) - 1] - data['timestamps'][0]) / 1000))
    data = data[ch_col_names].values.T
    # convert ultravolt to volt, since RawArray expects Volts for eeg kind. 1uv == (10^-6) * (1 Volt)
    data *= 1e-6
    info = mne.create_info(ch_names=ch_col_names, ch_types=ch_col_types, sfreq=sfreq, montage=montage)
    return mne.io.RawArray(data=data, info=info)


def print_histogram(df):
    df = df.drop(['timestamps', "timestamp_readable", 'Stim'], axis=1)
    df.plot.hist(alpha=0.5)
    plt.show()


def concatenate_df(path):
    paths = glob(path)
    dfs = []

    for p in paths:
        df = pd.read_csv(p, index_col=None, header=0)
        dfs.append(df)
    return pd.concat(dfs)


def plot_psd(files):
    raw = raw_from_path(files)
    raw.plot_psd(tmax=np.inf)


def plot_raw_data(raw, events):
    if events is not None:
        raw.plot(n_channels=4, events=events, scalings={'eeg': 2e-04}, title='EEG data', show=True, block=True)
    else:
        raw.plot(n_channels=4, scalings={'eeg': 2e-04}, title='EEG data', show=True, block=True)

# # dff = concatenate_df('/Users/shiran/workspace/eeg-processing/raw-data/p300/*.*')
# path = '/Users/shiran/workspace/eeg-processing/raw-data/p300/02-10-18_13-49-40.csv'
# #
# dff = concatenate_df(path)
# raw = raw_from_df(dff)
# raw.plot_psd(tmax=np.inf)

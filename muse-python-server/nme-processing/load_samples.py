from glob import glob

from mne import create_info
from mne.channels import read_montage

import pandas as pd
from mne.io import RawArray

subject = 1
session = 1
raw = []
fnames = glob('/Users/shiran/workspace/muse-lsl/data/visual/P300/subject%s/session%s/data_*.csv' % (subject, session))
raw = []
for fname in fnames:
    # read the file
    data = pd.read_csv(fname, index_col=0)
    raw.append(data)
    sfreq = 256

    ch_names = list(data.columns)[0:4] + ['Stim']
    ch_types = ['eeg'] * 4 + ['stim']
    montage = read_montage('standard_1005')
    data = data.values[:, [0, 1, 2, 3, 5]].T
    data[:-1] *= 1e-6
    info = create_info(ch_names=ch_names, ch_types=ch_types, sfreq=sfreq, montage=montage)
    raw.append(RawArray(data=data, info=info))

print(data.shape)
# name of each channels

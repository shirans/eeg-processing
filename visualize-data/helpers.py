import datetime
import numpy as np
import traceback


def print_time_diff(timestamps):
    from_timestamp = datetime.datetime.fromtimestamp(timestamps[0])
    to_timestamp = datetime.datetime.fromtimestamp(timestamps[- 1])
    print from_timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], to_timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]


def roll_with_new_data(data, samples, time_x, time_sample):
    try:
        nd_samples = np.array(samples).transpose()
        new_data = np.hstack((nd_samples, data))
        new_time = np.hstack((np.array(time_sample), time_x))
        return new_data[:, :data.shape[1]], new_time[:len(time_x)]
    except ValueError:
        traceback.print_exc()
        return data, time_x

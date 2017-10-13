import numpy as np
import traceback
import time
import datetime

from pylsl import pylsl


def print_time_diff(timestamps):
    from_timestamp = datetime.datetime.fromtimestamp(timestamps[0])
    to_timestamp = datetime.datetime.fromtimestamp(timestamps[- 1])
    print from_timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], to_timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]


def roll_with_new_data(data, samples, time_x, time_sample):
    try:
        if len(samples) != len(time_sample):
            print("samples are not the same length as data!")
            return
        nd_samples = np.array(samples).transpose()
        flipped = np.fliplr(nd_samples)
        new_data = np.hstack((flipped, data))
        time_sample.reverse()
        new_time = np.hstack((np.array(time_sample), time_x))
        return new_data[:, :data.shape[1]], new_time[:len(time_x)]
    except ValueError:
        traceback.print_exc()
        return data, time_x


def current_milli_time():
    millis = int(round(time.time() * 1000))
    return millis


def local_clock():
    return pylsl.local_clock()


def my_time():
    return time.time()


f = my_time()
clock = local_clock()
print "{} {}".format(datetime.datetime.fromtimestamp(clock), datetime.datetime.fromtimestamp(f))

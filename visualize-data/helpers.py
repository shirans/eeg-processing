import datetime


def print_time_diff(timestamps):
    from_timestamp = datetime.datetime.fromtimestamp(timestamps[0])
    to_timestamp = datetime.datetime.fromtimestamp(timestamps[- 1])
    print from_timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], to_timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

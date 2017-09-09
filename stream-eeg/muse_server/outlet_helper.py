from uuid import uuid4

from pylsl import StreamInfo, StreamOutlet, XMLElement

MUSE = 'Muse'

STREAM_TYPE = 'EEG'
SAMPLE_RATE = 256  # Muse 2016 only uses 256MH
CHANNELS_COUNT = 5
CHANNELS_NAMES = ['TP9', 'AF7', 'AF8', 'TP10', 'RIGHT AUX']


def create_cahnnels():
    info = StreamInfo(MUSE, STREAM_TYPE, CHANNELS_COUNT, SAMPLE_RATE, 'float32')
    channels = info.desc().append_child("channels")

    for channel in CHANNELS_NAMES:
        channels.append_child("channel") \
            .append_child_value("label", channel)
    return channels


CHANNELS = create_cahnnels()


def get_outlet(unique_id):
    info = StreamInfo(MUSE, STREAM_TYPE, CHANNELS_COUNT, SAMPLE_RATE, 'float32', unique_id)
    info.desc().append_child_value("manufacturer", "Muse")
    channels_2 = create_cahnnels()
    info.desc().prepend_copy(channels_2)

    # muse monitor does not pack in 12 bit resolution, no need for   StreamOutlet(info,12,360)
    outlet = StreamOutlet(info)
    return outlet


def get_outlet_random_id():
    return get_outlet(str(uuid4()))

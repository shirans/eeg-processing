from uuid import uuid4

from pylsl import StreamInfo, StreamOutlet

STREAM_TYPE = 'EEG'


def get_outlet(unique_id):
    info = StreamInfo('Muse', STREAM_TYPE, 5, 256, 'float32', unique_id)

    info.desc().append_child_value("manufacturer", "Muse")
    channels = info.desc().append_child("channels")

    for c in ['TP9', 'AF7', 'AF8', 'TP10', 'Right AUX']:
        channels.append_child("channel") \
            .append_child_value("label", c) \
            .append_child_value("unit", "microvolts") \
            .append_child_value("type", "EEG")
    # muse monitor does not pack in 12 bit resolution, no need for   StreamOutlet(info,12,360)
    outlet = StreamOutlet(info)
    return outlet


def get_outlet_random_id():
    return get_outlet(str(uuid4()))

from uuid import uuid4
from pylsl import StreamInfo, StreamOutlet, XMLElement, resolve_byprop, StreamInlet
import logging

from muse_stream_info import MuseStreamInfo

logger = logging.getLogger(__name__)

MUSE = 'Muse'

STREAM_TYPE = 'EEG'
SAMPLE_RATE = 256  # Muse 2016 only uses 256MH
CHANNELS_COUNT = 5
CHANNELS_NAMES = ['TP9', 'AF7', 'AF8', 'TP10', 'Right AUX']
NUM_EVENTS_PER_POLL = 12

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


def get_marker_info(uuid):
    return StreamInfo('Markers', 'Markers', 1, 0, channel_format='string', source_id=uuid)


def get_marker_info_random_id():
    return get_marker_info(str(uuid4()))

def push_sample_to_stream(out, tp9, af7, af8, tp10, right_aux):
    out.push_sample([tp9, af7, af8, tp10, right_aux])


def push_sample_to_stream_with_time(out, tp9, af7, af8, tp10, right_aux, l_clock):
    out.push_sample([tp9, af7, af8, tp10, right_aux], l_clock)


def find_stream(timeout=1):
    logger.info("searching for EEG stream for {} seconds".format(timeout))
    streams = resolve_byprop('type', STREAM_TYPE, timeout)
    if len(streams) == 0:
        logger.error("could not find stream")
        return
    print("found a stream")
    logger.info("found a stream")
    info = streams[0]

    inlet = StreamInlet(info, max_chunklen=12)

    info = inlet.info()
    description = info.desc()
    name = info.name()
    type = info.type()
    channels_count = info.channel_count()

    ch = description.child('channels').first_child()
    ch_names = [ch.child_value('label')]

    for i in range(channels_count - 1):
        ch = ch.next_sibling()
        ch_names.append(ch.child_value('label'))

    if name != MUSE or type != STREAM_TYPE or channels_count != CHANNELS_COUNT or ch_names != CHANNELS_NAMES:
        raise RuntimeError(
            "found an unexpected stream name:{} type:{} channels:{} ".format(name, type, ch_names))
    sd = MuseStreamInfo(inlet, info.nominal_srate(), channels_count)
    return sd


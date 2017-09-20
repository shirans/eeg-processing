from threading import Thread
import logging.config

import seaborn as sns
import matplotlib.pyplot as plt
from pylsl import resolve_byprop, StreamInlet

from muse_server import outlet_helper
from muse_server.outlet_helper import STREAM_TYPE, CHANNELS_NAMES
from stream_info import StreamInfo
from fig_info import FigInfo

sns.set_style("whitegrid", {'axes.grid': False})

logger = logging.getLogger(__name__)


# sns.despine(left=True)

class EegVisualizer:
    def __init__(self, timeout=1):
        self.timeout = timeout
        self.stream_details = None
        self.fig_info = None
        self.timestamps = None

    def find_stream(self, is_use_input_info=False):
        logger.info("searching for EEG stream for {} seconds".format(self.timeout))
        streams = resolve_byprop('type', STREAM_TYPE, self.timeout)
        if len(streams) == 0:
            logger.error("could not find stream")
            return
        logger.info("found a stream")
        info = streams[0]

        inlet = StreamInlet(info, max_buflen=1, max_chunklen=1)

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

        if name != outlet_helper.MUSE or type != outlet_helper.STREAM_TYPE or channels_count != outlet_helper.CHANNELS_COUNT or ch_names != CHANNELS_NAMES:
            raise RuntimeError(
                'found an unexpected stream name:{} type:{} channels:{} '.format(name, type, ch_names))
        sd = StreamInfo(inlet, info.nominal_srate(), channels_count)
        return sd

    def stop(self):
        self.fig_info.is_running = False

    def start(self):
        self.stream_details = self.find_stream()
        self.fig_info = FigInfo(self.stream_details.frequency, self.stream_details.channels_count)
        self.lunch_plot()

    def plot_graph(self):
        self.fig_info.plot(self.stream_details)

    def lunch_plot(self):
        plotting_thread = Thread(target=self.plot_graph)
        plotting_thread.daemon = False
        plotting_thread.start()
        plt.show()

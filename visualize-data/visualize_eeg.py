from threading import Thread
from time import sleep
import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt

from pylsl import resolve_byprop, StreamInlet

import logging.config

import outlet_helper
from outlet_helper import STREAM_TYPE

logger = logging.getLogger(__name__)
sns.set(style="whitegrid")


class EegVisualizer:
    def __init__(self, timeout=1):
        self.timeout = timeout
        self.stream = None
        self.fig = None
        self.timestamps = None
        self.is_running = True

    def on_key(self, event):
        print('you pressed', event.key, event.xdata, event.ydata)

        if event.key == 'q':
            self.is_running = False

    def find_stream(self):
        logger.info("searching for EEG stream for {} seconds".format(self.timeout))
        streams = resolve_byprop('type', STREAM_TYPE, self.timeout)
        if len(streams) == 0:
            logger.error("could not find stream")
            return
        logger.info("found a stream")
        inlet = StreamInlet(streams[0], max_chunklen=360)

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

        if name != outlet_helper.MUSE or type != outlet_helper.STREAM_TYPE or channels_count != outlet_helper.CHANNELS_COUNT or ch_names != outlet_helper.CHANNELS_NAMES:
            raise RuntimeError(
                'found an unexpected stream name:{} type:{} channels:{} '.format(name, type, ch_names))

        return inlet

    def stop(self):
        self.is_running = False

    def plot_graph(self):
        logger.debug("updating plot")
        t = 0
        while self.is_running:
            t = t + 1

    def start(self):
        inlet = self.find_stream()

        self.ch_names = ch_names

        self.init_fig()
        self.lunch_plot()

    def lunch_plot(self):
        plotting_thread = Thread(target=self.plot_graph)
        plotting_thread.daemon = True
        plotting_thread.start()
        plt.show()

    def init_fig(self):
        fig = plt.figure(figsize=plt.figaspect(0.5))
        ax = fig.add_subplot(111)
        ax.plot([1, 2, 3, 4], [10, 20, 25, 30], color='lightblue', linewidth=3)
        ax.scatter([0.3, 3.8, 1.2, 2.5], [11, 25, 9, 26], color='darkgreen', marker='^')
        ax.set_xlim(0.5, 4.5)
        fig.canvas.mpl_connect('key_press_event', self.on_key)

from threading import Thread
import logging.config

import seaborn as sns
import matplotlib.pyplot as plt
from pylsl import resolve_byprop, StreamInlet

from muse_server import outlet_helper
from muse_server.outlet_helper import STREAM_TYPE, CHANNELS_NAMES, find_stream
from muse_stream_info import MuseStreamInfo
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

    def stop(self):
        self.fig_info.is_running = False

    def start(self):
        self.stream_details = find_stream()
        self.fig_info = FigInfo(self.stream_details.frequency, self.stream_details.channels_count)
        self.lunch_plot()

    def plot_graph(self):
        self.fig_info.plot(self.stream_details)

    def lunch_plot(self):
        plotting_thread = Thread(target=self.plot_graph)
        plotting_thread.daemon = False
        plotting_thread.start()
        plt.show()

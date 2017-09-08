from threading import Thread
from time import sleep

import matplotlib.pyplot as plt

from pylsl import resolve_byprop, StreamInlet

import logging.config

from outlet_helper import STREAM_TYPE

logger = logging.getLogger(__name__)


class EegVisualizer:
    def __init__(self, timeout=1, max_chunklen=1):
        self.max_chunklen = max_chunklen
        self.timeout = timeout
        self.stream = None
        self.fig = None
        self.timestamps = None

    def find_stream(self):
        logger.info("searching for EEG stream for {} seconds".format(self.timeout))
        streams = resolve_byprop('type', STREAM_TYPE, self.timeout)
        if len(streams) == 0:
            logger.error("could not find stream")
            return
        logger.info("found a stream")
        self.stream = EegStream(streams[0], self.max_chunklen)
        # self.fig, self.axes = plt.subplots(1, 1, figsize={15, 6}, sharex=True)

    def plot_graph(self):
        logger.debug("updating plot")
        while True:
            logger.info("thread is running")
            sleep(3)

    def start(self):
        self.find_stream()
        thread = Thread(target=self.plot_graph)
        thread.daemon = True
        thread.start()


class EegStream:
    def __init__(self, stream, max_chunklen=1):
        self.inlet = StreamInlet(stream, max_chunklen=max_chunklen)

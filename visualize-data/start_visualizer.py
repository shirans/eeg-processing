import threading
from logging.config import dictConfig
import matplotlib.pyplot as plt

from pylsl import resolve_byprop
import logging

import logging_configs
from dummy_server.dummy_server import DummyServer

from visualize_eeg import EegVisualizer

logger = logging_configs.getMyLogger(__name__)


def startVisualize(eeg_server):
    eeg_server.start()
    v = EegVisualizer()
    v.start()
    plt.show()


if __name__ == "__main__":
    print "start"
    # server = BleDongleServer('/dev/cu.usbmodem1', "00:55:DA:B3:1A:3E")
    server = DummyServer()
    startVisualize(server)

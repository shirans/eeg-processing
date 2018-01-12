from threading import Thread

import numpy as np
import pandas as pd

from common import helpers
from logging_configs import getMyLogger
from muse_server.outlet_helper import NUM_EVENTS_PER_POLL, find_stream, CHANNELS_NAMES

logger = getMyLogger(__name__)


class DataRecorder:
    def __init__(self, data_type, timeout=1, num_events_per_poll=NUM_EVENTS_PER_POLL):
        self.is_running = True
        self.data_type = data_type
        self.stream_details = find_stream(1)
        self.timestamps = []
        self.samples = []
        self.counter = 0
        self.num_events_per_poll = num_events_per_poll

    def listen_input_stream(self):
        while self.is_running:
            samples, timestamps = self.stream_details.inlet.pull_chunk(
                timeout=1.0, max_samples=self.num_events_per_poll)

            self.timestamps.extend(timestamps)
            self.samples.extend(samples)
            self.counter += 1

    def dump_to_file(self):
        timestamps = self.timestamps
        samples = self.samples
        as_col = np.column_stack([timestamps, samples])
        df = pd.DataFrame(as_col, columns=[['t'] + CHANNELS_NAMES])
        path = helpers.get_output_path(self.data_type.name)
        df.to_csv(path, float_format='%.3f', index=False)
        print "saved {} batches with {},{} evnets".format(self.counter, len(samples), len(timestamps))

    def start_record(self):
        plotting_thread = Thread(target=self.listen_input_stream)
        plotting_thread.daemon = False
        plotting_thread.start()

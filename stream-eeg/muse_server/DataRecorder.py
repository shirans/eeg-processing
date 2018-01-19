from threading import Thread
from time import sleep

import numpy as np
import pandas as pd

from common import helpers
from constants import DataRecordType
from logging_configs import getMyLogger
from muse_server.outlet_helper import NUM_EVENTS_PER_POLL, find_stream, CHANNELS_NAMES
import datetime

logger = getMyLogger(__name__)


def data_recorder_controller(server, record_interval):
    recorder = DataRecorder(DataRecordType.plain_record)
    recorder.start_record()
    logger.info("waiting for init")
    while not server.is_init:
        sleep(2)
    logger.info("waiting for {} seconds to dump".format(record_interval))
    sleep(record_interval)
    logger.info("dumping to file")
    recorder.dump_to_file(add_readable_timestamp=True)
    server.stop()


class DataRecorder:
    def __init__(self, data_type, timeout=1, num_events_per_poll=NUM_EVENTS_PER_POLL):
        self.is_running = True
        self.data_type = data_type
        self.stream_details = find_stream(1)
        self.timestamps = []
        self.samples = []
        self.samples_sized = []
        self.counter = 0
        self.num_events_per_poll = num_events_per_poll

    def listen_input_stream(self):
        while self.is_running:
            samples, timestamps = self.stream_details.inlet.pull_chunk(
                timeout=1.0, max_samples=self.num_events_per_poll)

            self.timestamps.extend(timestamps)
            self.samples_sized.append(len(samples))
            self.samples.extend(samples)
            self.counter += 1

    def dump_to_file(self, add_readable_timestamp=False):
        timestamps = self.timestamps
        samples = self.samples
        if len(self.timestamps) == 0:
            logger.warn("no data to dump")
            return
        if add_readable_timestamp:
            timestamps_readable = map(lambda x:
                                      datetime.datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S.%f'), timestamps)
            as_col = np.column_stack([timestamps, timestamps_readable, samples])
            df = pd.DataFrame(as_col, columns=[['timesamps'] + ["timestamp_readable"] + CHANNELS_NAMES])
        else:
            as_col = np.column_stack([timestamps, samples])
            df = pd.DataFrame(as_col, columns=[['timesamps'] + CHANNELS_NAMES])
        path = helpers.get_output_path(self.data_type.name)
        df.to_csv(path, float_format='%.3f', index=False)
        logger.info("saved {} batches with {} evnets to path: {}".format(self.counter, len(samples), path))

    def start_record(self):
        logger.info("recording started")
        plotting_thread = Thread(target=self.listen_input_stream)
        plotting_thread.daemon = False
        plotting_thread.start()

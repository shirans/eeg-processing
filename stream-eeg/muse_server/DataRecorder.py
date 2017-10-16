from threading import Thread
import numpy as np
from muse_server.outlet_helper import NUM_EVENTS_PER_POLL, find_stream
import logging

logger = logging.getLogger(__name__)


class DataRecorder:
    def __init__(self, timeout=1, num_events_per_poll=NUM_EVENTS_PER_POLL):
        self.is_running = True
        self.stream_details = find_stream(1)
        self.timestamps = []
        self.samples = []
        self.num_events_per_poll = num_events_per_poll

    def listen_input_stream(self):
        while self.is_running:
            samples, timestamps = self.stream_details.inlet.pull_chunk(
                timeout=1.0, max_samples=self.num_events_per_poll)
        self.timestamps.extend(timestamps)
        self.samples.append(samples)

    def dump_to_file(self):
        correction = self.stream_details.inlet.time_correction()
        timestamps = np.array(self.timestamps) + correction
        logger.info("adding time correction to timestamps: {}".format(correction))

    def start_record(self):
        plotting_thread = Thread(target=self.listen_input_stream)
        plotting_thread.daemon = False
        plotting_thread.start()

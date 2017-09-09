import random
import logging
import thread

import threading
from threading import Thread
from time import sleep

from pylsl import local_clock

from logging_configs import getMyLogger
from outlet_helper import get_outlet_random_id, SAMPLE_RATE
from streaming_server import StreamingServer

logger = getMyLogger(__name__)


class ShutDownThread(Thread):
    def __init__(self, server):
        super(ShutDownThread, self).__init__()
        self.server = server

    def run(self):
        logger.info("press any key to stop the server")
        con = True
        while con:
            try:
                a = raw_input()
                con = False
                self.server.stop()
            except KeyboardInterrupt:
                con = False
                self.event.clear()


class DummyServer(StreamingServer):
    def __init__(self, is_daemon=True):
        self.event = threading.Event()
        self.running = True
        self.is_daemon = is_daemon

    def stop(self):
        self.running = False
        logger.info("Dummy server is stopped")

    def measure_response_time(self, num_iteration):
        pass

    def start(self):
        server_thread = Thread(target=self.send_eeg)
        server_thread.daemon = self.is_daemon
        server_thread.start()

        if not self.is_daemon:
            listening_thread = ShutDownThread(self)
            listening_thread.daemon = self.is_daemon
            listening_thread.start()

    def send_eeg(self):
        logger.info("Dummy server is starting to send data")
        out = get_outlet_random_id()
        sleep_interval = 1/SAMPLE_RATE
        while self.running:
            tp9 = random.uniform(-100.0, 100.0)
            af7 = random.uniform(-100.0, 100.0)
            af8 = random.uniform(-100.0, 100.0)
            tp10 = random.uniform(-100.0, 100.0)
            right_aux = random.uniform(-100.0, 100.0)
            osc_time = local_clock()
            out.push_sample([tp9, af7, af8, tp10, right_aux], osc_time)
            sleep(sleep_interval)
        logger.info("Dummy server stopped sending data")

import random
import logging
import thread

import threading
from threading import Thread
from time import sleep

from pylsl import local_clock

from logging_configs import getMyLogger
from outlet_helper import get_outlet_random_id
from streaming_server import StreamingServer

logger = getMyLogger(__name__)


class ShutDownThread(Thread):
    def __init__(self, server):
        super(ShutDownThread, self).__init__()
        self.server = server

    def run(self):
        con = True
        while con:
            try:
                a = raw_input()
                con = False
                self.server.stop()
                logger.info("stop")
            except KeyboardInterrupt:
                con = False
                self.event.clear()
                logger.info("stop interrup")


class DummyServer(StreamingServer):
    def __init__(self):
        self.event = threading.Event()
        self.running = True

    def stop(self):
        self.running = False
        logger.info("Dummy server is stopped")

    def measure_response_time(self, num_iteration):
        pass

    def start(self):
        server_thread = Thread(target=self.send_eeg)
        server_thread.daemon = False
        server_thread.start()

        listening_thread = ShutDownThread(self)
        listening_thread.daemon = False
        listening_thread.start()

    def send_eeg(self):
        logger.info("Dummy server is starting to send data")
        out = get_outlet_random_id()
        while self.running:
            for i in range(1, 10):
                tp9 = random.uniform(-100.0, 100.0)
                af7 = random.uniform(-100.0, 100.0)
                af8 = random.uniform(-100.0, 100.0)
                tp10 = random.uniform(-100.0, 100.0)
                right_aux = random.uniform(-100.0, 100.0)
                osc_time = local_clock()
                out.push_sample([tp9, af7, af8, tp10, right_aux], osc_time)
            sleep(1)
        logger.info("Dummy server stopped sending data")

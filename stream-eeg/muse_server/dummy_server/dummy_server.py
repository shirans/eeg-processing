import threading
from abc import abstractmethod
from threading import Thread


from logging_configs import getMyLogger
from muse_server.streaming_server import StreamingServer

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

    @abstractmethod
    def send_eeg(self):
        pass
import traceback
from abc import abstractmethod
import logging
import sys

logger = logging.getLogger(__name__)


class StreamingServer(object):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def measure_response_time(self, num_iteration):
        pass


def start_server(server):
    print("Starting muse monitor dongle server. python version: " + sys.version)
    try:
        server.start()
    except KeyboardInterrupt:
        print("exit due to use click")  # do cleanup here
    except Exception as e:
        logging.error(traceback.format_exc())
        logging.error(e)
    finally:
        print("Closing server")
        if server is not None:
            server.stop()

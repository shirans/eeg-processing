import traceback
from abc import abstractmethod
import logging_configs
import sys
import logging


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
        logger.warn(traceback.format_exc())
    finally:
        print("Closing server")
        if server is not None:
            server.stop()

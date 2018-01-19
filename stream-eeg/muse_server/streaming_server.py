import threading
import traceback
from abc import abstractmethod
from threading import Thread

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
    def is_init(self):
        pass

    @abstractmethod
    def measure_response_time(self, num_iteration):
        pass


def start_server(server):
    print("Starting muse monitor dongle server. python version: " + sys.version)
    print("thread: {}".format(threading.currentThread().name))
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


def start_server_new_thread(server):
    server_thread = Thread(target=start_server,kwargs= {'server': server})
    server_thread.daemon = False
    server_thread.start()


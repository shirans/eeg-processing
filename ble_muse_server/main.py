#!/usr/bin/env python2.7
import logging
import sys
import traceback

from BleDonbgleServer import BleDongleServer
logger = logging.getLogger(__name__)

def start_ble_dongle_server():
    print("Starting ble dongle server. ptyhon verison: " + sys.version)
    server = BleDongleServer('/dev/cu.usbmodem1', "00:55:DA:B3:1A:3E")
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


if __name__ == "__main__":
    start_ble_dongle_server()

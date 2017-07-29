#!/usr/bin/env python2.7
import logging

import streaming_server
from ble_muse_server.BleDonbgleServer import BleDongleServer

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    streaming_server.start_server(BleDongleServer('/dev/cu.usbmodem1', "00:55:DA:B3:1A:3E"))

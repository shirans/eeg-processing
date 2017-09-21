#!/usr/bin/env python2.7

import streaming_server
from ble_muse_server.BleDonbgleServer import BleDongleServer

if __name__ == "__main__":
    streaming_server.start_server(BleDongleServer('/dev/cu.usbmodem1'))

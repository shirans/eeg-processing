#!/usr/bin/env python3

import streaming_server
from muse_monitor_server.MuseMonitorServer import MuseMonitorServer

if __name__ == "__main__":
    server = MuseMonitorServer(ip="10.0.0.1", port=8001, unique_id="00:55:DA:B3:1A:3E")
    streaming_server.start_server(server)

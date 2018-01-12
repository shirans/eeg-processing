#!/usr/bin/env python3

import streaming_server
from muse_monitor_server.MuseMonitorServer import MuseMonitorServer


def start_muse_monitor_server(ip, port, unique_id):
    server = MuseMonitorServer(ip=ip, port=port, unique_id=unique_id, server_type=None)
    streaming_server.start_server(server)


if __name__ == "__main__":
    start_muse_monitor_server(ip="10.0.0.4", port=8001, unique_id="00:55:DA:B3:1A:3E")

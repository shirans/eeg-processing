from muse_server.ble_muse_server.BleDonbgleServer import BleDongleServer
from muse_server.dummy_server.ArtificialEeg import ArtificialEeg, SignalType
from muse_server.dummy_server.file_player_server import FilePlayerServer
from enum import Enum
from muse_server import streaming_server


class StreamDataInputType(Enum):
    muse = 0,
    from_file = 1,
    generate_random_data = 2,
    generate_straight_line = 3


def start_server(input_type):
    # This file starts to stream data and dumps it into a file.
    server = None
    if input_type == StreamDataInputType.muse:
        server = BleDongleServer('/dev/cu.usbmodem1', "00:55:DA:B3:1A:3E")
        streaming_server.start_server_new_thread(server)
    elif input_type == StreamDataInputType.from_file:
        FilePlayerServer().start()
    elif input_type == StreamDataInputType.generate_straight_line:
        ArtificialEeg(signalType=SignalType.Line).start()
    else:
        ArtificialEeg(signalType=SignalType.Random).start()
    return server

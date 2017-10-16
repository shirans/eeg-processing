from time import sleep

from muse_server import streaming_server
from muse_server.DataRecorder import DataRecorder
from muse_server.ble_muse_server.BleDonbgleServer import BleDongleServer
from muse_server.dummy_server.ArtificialEeg import ArtificialEeg, SignalType
from visualize_eeg import EegVisualizer

if __name__ == "__main__":
    # FilePlayerServer().start()
    ArtificialEeg(signalType=SignalType.Line).start()
    #streaming_server.start_server_new_thread(BleDongleServer('/dev/cu.usbmodem1', "00:55:DA:B3:1A:3E"))
    EegVisualizer().start()
    # recorder = DataRecorder()
    # recorder.start_record()
    # sleep(1)
    # recorder.dump_to_file()

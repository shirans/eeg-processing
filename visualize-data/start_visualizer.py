from muse_server.dummy_server.file_player_server import FilePlayerServer
from muse_server.dummy_server.random_eeg import RandomEeg
from visualize_eeg import EegVisualizer

if __name__ == "__main__":
    FilePlayerServer().start()
    #RandomEeg().start()
    v = EegVisualizer()
    v.start()

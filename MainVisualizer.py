from StreamingServer import StreamDataInputType, start_server
from visualize_eeg import EegVisualizer

if __name__ == "__main__":
    start_server(StreamDataInputType.muse)
    EegVisualizer().start()
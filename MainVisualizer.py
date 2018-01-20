from StreamingServer import StreamDataInputType, start_server
from visualize_eeg import EegVisualizer

if __name__ == "__main__":
    start_server(StreamDataInputType.muse)
    EegVisualizer(boundaries={'min': 0, 'max': 2048}).start()

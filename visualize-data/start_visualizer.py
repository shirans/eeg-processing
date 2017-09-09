from dummy_server.dummy_server import DummyServer
from visualize_eeg import EegVisualizer

if __name__ == "__main__":
    DummyServer().start()
    v = EegVisualizer()
    v.start()

from time import sleep, time

from logging_configs import getMyLogger
from muse_server.dummy_server.dummy_server import DummyServer
from muse_server.outlet_helper import get_outlet_random_id, SAMPLE_RATE

logger = getMyLogger(__name__)
from glob import glob


class FilePlayerServer(DummyServer):
    def __init__(self, is_deamon=True):
        super(FilePlayerServer, self).__init__(is_deamon)

    def send_eeg(self):
        sleep(1)
        lines = [line.rstrip('\n') for line in open(glob('../raw-data/*.csv')[0])]
        out = get_outlet_random_id()
        logger.info("Dummy server is starting to send data")
        sleep_interval = 1 / SAMPLE_RATE
        i = 0
        while self.running:
            for line in lines[1:]:
                if not self.running:
                    break
                i += 1
                data = line.split(",")
                tp9 = float(data[1])
                af7 = float(data[2])
                af8 = float(data[3])
                tp10 = float(data[4])
                right_aux = float(data[5])
                osc_time = time()
                out.push_sample([tp9, af7, af8, tp10, right_aux], osc_time)
                sleep(sleep_interval)
        logger.info("Dummy server stopped sending data")

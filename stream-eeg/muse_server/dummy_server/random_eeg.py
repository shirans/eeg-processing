import random
from time import sleep, time

from dummy_server import DummyServer
from logging_configs import getMyLogger
from muse_server.outlet_helper import get_outlet_random_id, SAMPLE_RATE

logger = getMyLogger(__name__)


class RandomEeg(DummyServer):
    def send_eeg(self):
        logger.info("Dummy server is starting to send data")
        out = get_outlet_random_id()
        sleep_interval = 1. / SAMPLE_RATE
        print "sleep interval RandomEeg: {}".format(sleep_interval)
        i = 0
        while self.running:
            i+=1
            tp9 = random.uniform(-100.0, 100.0)
            af7 = random.uniform(-100.0, 100.0)
            af8 = random.uniform(-100.0, 100.0)
            tp10 = random.uniform(-100.0, 100.0)
            right_aux = random.uniform(-100.0, 100.0)
            osc_time = time()
            # print "server", osc_time,  datetime.datetime.fromtimestamp(osc_time).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            out.push_sample([tp9, af7, af8, tp10, right_aux], osc_time)
            # print "{}".format(i)
            # sleep(sleep_interval)

    def __init__(self, is_daemon=True):
        super(RandomEeg, self).__init__(is_daemon)

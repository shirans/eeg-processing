import random
from time import sleep

from enum import Enum
from pylsl import local_clock

from common.helpers import current_milli_time
from dummy_server import DummyServer
from logging_configs import getMyLogger
from muse_server.outlet_helper import get_outlet_random_id, SAMPLE_RATE, push_sample_to_stream_with_time

logger = getMyLogger(__name__)


class SignalType(Enum):
    Random = 1
    Line = 2


def push_data(tp9, af7, af8, tp10, right_aux, prev_clock, sleep_interval, out):
    osc_time = current_milli_time()
    l_clock = local_clock()
    if prev_clock > local_clock():
        print " jump in time"
    # print "server", osc_time,  datetime.datetime.fromtimestamp(osc_time).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    push_sample_to_stream_with_time(out, tp9, af7, af8, tp10, right_aux, l_clock)
    sleep(sleep_interval)


class ArtificialEeg(DummyServer):
    def send_eeg(self):
        logger.info("Dummy server is starting to send data")
        out = get_outlet_random_id()
        sleep_interval = 1. / SAMPLE_RATE
        logger.info("sleep interval RandomEeg: {}".format(sleep_interval))

        prev_clock = local_clock()
        if self.signalType is SignalType.Line:
            self.generate_line_signal(prev_clock, sleep_interval, out)
        else:
            self.generate_random_signal(out, prev_clock, sleep_interval)

    def generate_random_signal(self, out, prev_clock, sleep_interval):
        i = 0
        while self.running:
            i += 1
            tp9 = random.uniform(-100.0, 100.0)
            af7 = random.uniform(-100.0, 100.0)
            af8 = random.uniform(-100.0, 100.0)
            tp10 = random.uniform(-100.0, 100.0)
            right_aux = random.uniform(-100.0, 100.0)
            push_data(tp9, af7, af8, tp10, right_aux, prev_clock, sleep_interval, out)

    def generate_line_signal(self, prev_clock, sleep_interval, out):
        curr = -100
        while self.running:
            if curr == 100.0:
                curr = -100
            tp9 = af7 = af8 = tp10 = right_aux = curr
            curr += 1
            push_data(tp9, af7, af8, tp10, right_aux, prev_clock, sleep_interval, out)

    def __init__(self, signalType=SignalType.Random, is_daemon=True):
        super(ArtificialEeg, self).__init__(is_daemon)
        self.signalType = signalType

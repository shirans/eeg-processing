import threading
from time import sleep

from pylsl import StreamOutlet, StreamInfo
import random

from StreamingServer import StreamDataInputType, start_server
from logging_configs import getMyLogger
from muse_server.DataRecorder import DataRecorder
from experiment.p300 import P300
from constants import WinSize
from muse_server.outlet_helper import get_marker_info_random_id

logger = getMyLogger(__name__)

if __name__ == "__main__":

    inputType = StreamDataInputType.muse
    num_iteration = 5
    server = start_server(inputType)

    logger.info("waiting for init")
    while not server.is_init:
        sleep(1)

    info = get_marker_info_random_id()
    outlet = StreamOutlet(info)
    recorder = DataRecorder("p300", marker_info=info, signal_marker='rare')
    recorder.start_record()

    options = ['cars', 'flowers', 'lamps', 'penguins']
    objs = random.sample(options, 2)

    targets = "/Users/shiran/workspace/stimulis/{}/*".format(objs[0])
    nontargs = "/Users/shiran/workspace/stimulis/{}/*".format(objs[1])
    P300(is_full_screen=True,
         win_size=WinSize(800, 600),
         targets=targets,
         nontargets=nontargs,
         lookup_name=objs[0],
         outlet=outlet,
         num_iteration=num_iteration).start_experiment()

    recorder.dump_to_file(add_readable_timestamp=True)
    recorder.close_stream()
    server.stop()

    logger.info("Experiment finished")

    main_thread = threading.current_thread()
    for t in threading.enumerate():
        if t is main_thread:
            continue
        logger.info('joining %s', t.getName())
        t.join()

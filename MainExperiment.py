from time import sleep

from pylsl import StreamOutlet, StreamInfo

from StreamingServer import StreamDataInputType, start_server
from logging_configs import getMyLogger
from muse_server.DataRecorder import DataRecorder
from experiment.p300 import P300
from constants import WinSize
from muse_server.outlet_helper import get_marker_info_random_id

logger = getMyLogger(__name__)

if __name__ == "__main__":

    inputType = StreamDataInputType.generate_straight_line
    record_interval = 10
    server = start_server(inputType)

    logger.info("waiting for init")
    while not server.is_init:
        sleep(2)

    info = get_marker_info_random_id()
    outlet = StreamOutlet(info)
    recorder = DataRecorder("p300", marker_info=info, signal_marker='rare')
    recorder.start_record()

    P300(is_full_screen=True,
         win_size=WinSize(800, 600),
         targets="/Users/shiran/workspace/stimulis/cars/*",
         nontargets="/Users/shiran/workspace/stimulis/flowers/*",
         outlet=outlet) \
        .start_experiment()

    recorder.dump_to_file(add_readable_timestamp=True)

    server.stop()

    logger.info("Experiment finished")

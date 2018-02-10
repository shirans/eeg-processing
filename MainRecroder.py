from StreamingServer import StreamDataInputType, start_server
from logging_configs import getMyLogger
from muse_server.DataRecorder import data_recorder_controller

logger = getMyLogger(__name__)

if __name__ == "__main__":
    inputType = StreamDataInputType.muse
    recordInterval = 5
    server = start_server(inputType)
    data_recorder_controller(server, recordInterval)

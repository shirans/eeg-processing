#!/usr/bin/env python3
import time
from pythonosc import dispatcher
from pythonosc import osc_server
from pylsl import local_clock

# tp9: left, behind the ear,
# af7: frontal left
# af8: frontal right
# tp10: right, behind the ear,
# right_aux
from streaming_server import StreamingServer
from pylsl import StreamInfo, StreamOutlet


def print_blinks_handler(unused_addr, blink):
    print(time.strftime("%x %X") + ": blink")


def print_waves_handler(unused_addr, tp9, af7, af8, tp10):
    print({"tp9": tp9, "tp10": tp10, "af7": af7, "af8": af8})


def eeg_handler(unused_addr, outlet, tp9, af7, af8, tp10, right_aux):
    # TODO: extract the real time!!!
    osc_time = local_clock()
    outlet[0].push_sample([tp9, af7, af8, tp10, right_aux], osc_time)


def get_outlet(unique_id):
    info = StreamInfo('Muse', 'EEG', 5, 256, 'float32', unique_id)

    info.desc().append_child_value("manufacturer", "Muse")
    channels = info.desc().append_child("channels")

    for c in ['TP9', 'AF7', 'AF8', 'TP10', 'Right AUX']:
        channels.append_child("channel") \
            .append_child_value("label", c) \
            .append_child_value("unit", "microvolts") \
            .append_child_value("type", "EEG")
    # muse monitor does not pack in 12 bit resolution, no need for   StreamOutlet(info,12,360)
    outlet = StreamOutlet(info)
    return outlet


# assuming Muse Monitor is streaming data
class MuseMonitorServer(StreamingServer):
    def __init__(self, ip, port, unique_id, server_type='threading'):
        self.unique_id = unique_id
        self.outlet = get_outlet(unique_id)
        self.ip = ip
        self.port = port
        self.disp = dispatcher.Dispatcher()
        self.server_type = server_type

        # register handlers
        self.disp.map("/muse/eeg", eeg_handler, self.outlet)
        self.disp.map("/muse/elements/blink", print_blinks_handler)
        # self.disp.map("/muse/elements/beta_absolute", print_waves_handler)
        # self.disp.map("/muse/elements/gamma_absolute", print_waves_handler)
        # self.disp.map("/muse/elements/delta_absolute", print_waves_handler)
        # self.disp.map("/muse/elements/theta_absolute", print_waves_handler)

        if server_type is None:
            self.server = osc_server.BlockingOSCUDPServer((self.ip, self.port), self.disp)
        else:
            self.server = osc_server.ThreadingOSCUDPServer((self.ip, self.port), self.disp)

    def start(self):
        print("Serving on {}".format(self.server.server_address))
        self.server.serve_forever()
        print(self.ip)

    def stop(self):
        self.server.server_close()

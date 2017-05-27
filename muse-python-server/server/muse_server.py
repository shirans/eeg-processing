from pythonosc import dispatcher
from pythonosc import osc_server

from server.stream_info import get_outlet


def eeg_handler(self, unused_addr, args, osc_time, tp9, af7, af8, tp10, right_aux):
    self.outlet.push_sample([tp9, af7, af8, tp10, right_aux], osc_time)


class MuseServer:
    def __init__(self, unique_id, ip, port):
        self.unique_id = unique_id
        self.outlet = get_outlet(unique_id)
        self.dispatcher = dispatcher.Dispatcher()
        self.ip = ip
        self.port = port

    def start_server(self):
        # dispatcher.map("/debug", print)
        self.dispatcher.map("/muse/eeg", eeg_handler, "EEG")
        # dispatcher.map("/muse/elements/alpha_absolute", print)
        # dispatcher.map("/muse/elements/beta_absolute", print)
        # dispatcher.map("/muse/elements/gamma_absolute", print)
        # dispatcher.map("/muse/elements/delta_absolute", print)
        # dispatcher.map("/muse/elements/theta_absolute", print)

        self.server = osc_server.ThreadingOSCUDPServer((self.ip, self.port), dispatcher)
        print("Serving on {}".format(self.server.server_address))
        self.server.serve_forever()

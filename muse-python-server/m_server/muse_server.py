from pythonosc import dispatcher
from pythonosc import osc_server
from m_server import stream_info
from pylsl import local_clock


# tp9: left, behind the ear,
# af7: frontal left
# af8: frontal right
# tp10: right, behind the ear,
# right_aux
def eeg_handler(unused_addr, outlet, tp9, af7, af8, tp10, right_aux):
    # TODO: extract the real time!!!
    osc_time = local_clock()
    outlet[0].push_sample([tp9, af7, af8, tp10, right_aux], osc_time)


class MuseServer:
    def __init__(self, unique_id, ip, port, server_type):
        self.unique_id = unique_id
        self.outlet = stream_info.get_outlet(unique_id)
        self.ip = ip
        self.port = port
        self.disp = dispatcher.Dispatcher()
        self.disp.map("/muse/eeg", eeg_handler, self.outlet)
        self.disp.map("/muse/elements/blink", print)
        # # dispatcher.map("/muse/elements/beta_absolute", print)
        # # dispatcher.map("/muse/elements/gamma_absolute", print)
        # # dispatcher.map("/muse/elements/delta_absolute", print)
        # # dispatcher.map("/muse/elements/theta_absolute", print)
        if server_type == 'threading':
            self.server = osc_server.ThreadingOSCUDPServer((self.ip, self.port), self.disp)
        else:
            self.server = osc_server.BlockingOSCUDPServer((self.ip, self.port), self.disp)

    def start_server(self):
        print("Serving on {}".format(self.server.server_address))
        self.server.serve_forever()
        print(self.ip)

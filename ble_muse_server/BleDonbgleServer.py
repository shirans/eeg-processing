import logging
import os
from threading import Thread
from time import sleep

import pygatt
import sys

# since Muse Monitor can only work with pthon3, the upper level package could no be setup as the project in pycharm
# sys.path.append(os.path.abspath('../muse_server'))
from muse_server.streaming_server import StreamingServer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BleDongleServer(StreamingServer):
    def __init__(self, serial_port, ip=None):
        self.ip = ip
        self.serial_port = serial_port
        self.adapter = pygatt.BGAPIBackend(serial_port=self.serial_port)
        self.device = None

    def find_ip(self):
        devices = self.adapter.scan()
        first_device = next((x for x in devices if 'muse' in x['name'].lower()), None)
        if first_device is None:
            return None
        ip = next((x for x in devices if 'muse' in x['name'].lower()), None)['address']
        logger.info("found device at address:{}. device data: {}".format(ip, first_device))
        return ip

    def start(self):
        self.adapter.start()
        if self.ip is None:
            ip = self.find_ip()
            if ip is None:
                logger.warning("could not file ip.")
                raise RuntimeError("could not file ip")
            self.ip = ip
        logger.info('connect server to ip {}'.format(self.ip))
        self.thread = Thread()
        self.thread.daemon = True
        self.thread.start()
        self.device = self.adapter.connect(self.ip)
        self.subscribe(self.device)
        # The 0x000e is the handle of the Client Characteristic Configuration (CCC) uuid 2902
        a = self.device.discover_characteristics()
        self.device.char_write_handle(0x000e, [0x02, 0x64, 0x0a], False)
        all_uuids = []
        for uuid, desc in a.iteritems():
            all_uuids.append("uuid: " + str(desc.uuid) + ", handle:" + str(desc.handle))
        print(all_uuids)

        while 1:
            try:
                logger.info("sleepuing")
                sleep(0.1)
            except KeyboardInterrupt:
                logger.info("got keyboard")
                break
            except:
                break

    def stop(self):
        if self.device is not None:
            self.device.disconnect()
            self.adapter.stop()

    def subscribe(self, device):
        device.subscribe('273e0003-4c4d-454d-96be-f03bac821358',
                         callback=self.handle_eeg)
        device.subscribe('273e0004-4c4d-454d-96be-f03bac821358',
                         callback=self.handle_eeg)
        device.subscribe('273e0005-4c4d-454d-96be-f03bac821358',
                         callback=self.handle_eeg)
        device.subscribe('273e0006-4c4d-454d-96be-f03bac821358',
                         callback=self.handle_eeg)
        device.subscribe('273e0007-4c4d-454d-96be-f03bac821358',
                         callback=self.handle_eeg)

    def handle_eeg(self, handle, data):
        print("got data: " + str(data))
        print("handle: " + str(handle))

        """Calback for receiving a sample.

        sample are received in this oder : 44, 41, 38, 32, 35
        wait until we get 35 and call the data
        """
        # print(data)
        # timestamp = self.time_func()
        # index = int((handle - 32) / 3)
        # tm, d = self._unpack_eeg_channel(data)
        # self.data[index] = d
        # self.timestamps[index] = timestamp
        # # last data received
        # if handle == 35:
        #     # affect as timestamps the first timestamps - 12 sample
        #     timestamps = np.arange(-12, 0) / 256.
        #     timestamps += np.min(self.timestamps)
        #     self.callback(self.data, timestamps)
        #     self._init_sample()

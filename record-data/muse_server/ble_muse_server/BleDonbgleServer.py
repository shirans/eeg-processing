import logging
import os
from threading import Thread
from time import sleep, time
import numpy as np
import bitstring
import datetime
import pygatt
import sys
from pylsl import StreamInfo, StreamOutlet

# since Muse Monitor can only work with pthon3, the upper level package could no be setup as the project in pycharm
from streaming_server import StreamingServer

sys.path.append(os.path.abspath('../muse_server'))
from pylsl import StreamInfo

logging.basicConfig(level=logging.INFO)
logging.getLogger('pygatt').setLevel(level=logging.WARN)
logger = logging.getLogger(__name__)


class BleDongleServer(StreamingServer):
    def __init__(self, serial_port, ip=None):
        self.ip = ip
        self.serial_port = serial_port
        self.adapter = pygatt.BGAPIBackend(serial_port=self.serial_port)
        self.device = None

        self.timestamps = np.zeros(5)
        self.data = np.zeros((5, 12))

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
                logger.info("sleeping")
                sleep(1)
            except KeyboardInterrupt:
                logger.info("got keyboard")
                break

    def stop(self):
        if self.device is not None:
            self.device.disconnect()
            self.adapter.stop()

    def subscribe(self, device):
        device.subscribe('273e0003-4c4d-454d-96be-f03bac821358', callback=self.raw_eeg)  # 32 -- 0x20
        device.subscribe('273e0004-4c4d-454d-96be-f03bac821358', callback=self.raw_eeg)  # 35 -- 0x23
        device.subscribe('273e0005-4c4d-454d-96be-f03bac821358', callback=self.raw_eeg)  # 38 -- 0x26
        device.subscribe('273e0006-4c4d-454d-96be-f03bac821358', callback=self.raw_eeg)  # 41 -- 0x29
        device.subscribe('273e0007-4c4d-454d-96be-f03bac821358', callback=self.raw_eeg)  # 44 -- 0x2c

        device.subscribe('273e0009-4c4d-454d-96be-f03bac821358', callback=self.print_data)  # 20 --
        device.subscribe('273e0002-4c4d-454d-96be-f03bac821358', callback=self.print_data)  # 29 --
        device.subscribe('273e0001-4c4d-454d-96be-f03bac821358', callback=self.print_data)  # 14 --
        device.subscribe('273e000b-4c4d-454d-96be-f03bac821358', callback=self.print_data)  # 26 --
        device.subscribe('00002a00-0000-1000-8000-00805f9b34fb', callback=self.print_data)  # 7 --
        device.subscribe('00002a01-0000-1000-8000-00805f9b34fb', callback=self.print_data)  # 9 --
        device.subscribe('00002a04-0000-1000-8000-00805f9b34fb', callback=self.print_data)  # 1 --
        device.subscribe('273e000a-4c4d-454d-96be-f03bac821358', callback=self.print_data)  # 23--
        device.subscribe('273e0008-4c4d-454d-96be-f03bac821358', callback=self.print_data)  # 17--

    def print_data(self, handle, data):
        try:
            # un packing
            aa = bitstring.Bits(bytes=data)
            pattern = "uint:16,uint:12,uint:12,uint:12,uint:12,uint:12,uint:12, \
                           uint:12,uint:12,uint:12,uint:12,uint:12,uint:12"
            res = aa.unpack(pattern)
            logger.info("handle: 0x%x   data: %s", handle, str(list(res)))
        except Exception as e:
            logger.exception("failed processing handle:0x%x ", handle)

    def raw_eeg(self, handle, data):
        try:
            aa = bitstring.Bits(bytes=data)
            pattern = "uint:16,uint:12,uint:12,uint:12,uint:12,uint:12,uint:12, \
                           uint:12,uint:12,uint:12,uint:12,uint:12,uint:12"
            res = aa.unpack(pattern)

            logger.info("handle: 0x%s   data: %s", handle, str(list(res)))
            timestamp = res[0]
            data = res[1:]
            # 12 bits on a 2 mVpp range
            data = 0.48828125 * (np.array(data) - 2048)

            timestamp = time()
            index = int((handle - 32) / 3)

            self.data[index] = data
            self.timestamps[index] = timestamp
            # last data received
            if handle == 35:
                # affect as timestamps the first timestamps - 12 sample
                timestamps = np.arange(-12, 0) / 256.
                timestamps += np.min(self.timestamps)
                self.process(self.data, timestamps)
                self._init_sample()
        except Exception as e:
            logger.exception("failed processing handle:0x%x ", handle)

    def _init_sample(self):
        """initialize array to store the samples"""
        self.timestamps = np.zeros(5)
        self.data = np.zeros((5, 12))

    def process(self, data, timestamps):
        info = info = StreamInfo('Muse', 'EEG', 5, 256, 'float32')

        info.desc().append_child_value("manufacturer", "Muse")
        channels = info.desc().append_child("channels")
        for c in ['TP9', 'AF7', 'AF8', 'TP10', 'Right AUX']:
            channels.append_child("channel") \
                .append_child_value("label", c) \
                .append_child_value("unit", "microvolts") \
                .append_child_value("type", "EEG")
        outlet = StreamOutlet(info, 12, 360)

        for ii in range(12):
            outlet.push_sample(data[:, ii], timestamps[ii])

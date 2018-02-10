import datetime
import os
import sys
from logging import DEBUG
from time import sleep, time
from uuid import uuid4

import bitstring
import numpy as np
import pygatt
from pylsl import StreamInfo, StreamOutlet

import logging_configs
from helpers import current_milli_time
from muse_server.streaming_server import StreamingServer

# since Muse Monitor can only work with pthon3, the upper level package could no be setup as the project in pycharm

sys.path.append(os.path.abspath('../muse_server'))

logger = logging_configs.getMyLogger(__name__)
logger.setLevel(level=DEBUG)

SUPPLY_VOLTAGE_P2P = 2.0 * 1000  # 2mv p peak t0 peak
ANALOG_VALUE_RANGE = 4096  # 2^12, each signal is 12 units
SIGNAL_SCALE = SUPPLY_VOLTAGE_P2P / ANALOG_VALUE_RANGE  # 0.48828125
PATTERN_SIGNED = "uint:16,int:12,int:12,int:12,int:12,int:12,int:12, \
                                    int:12,int:12,int:12,int:12,int:12,int:12"

PATTERN_UNSIGNED = "uint:16,uint:12,uint:12,uint:12,uint:12,uint:12,uint:12, \
                                    uint:12,uint:12,uint:12,uint:12,uint:12,uint:12"


def timed_action(device):
    a = device.get_rssi()


def parse_v1_unsigned_shifted_scaled(as_bits):
    data = as_bits.unpack(PATTERN_UNSIGNED)
    timestamp = data[0]
    data = np.array(data[1:])
    data = SIGNAL_SCALE * (np.array(data) - 2048)
    return timestamp, data


def parse_v2_signed_normalized(as_bits):
    data = as_bits.unpack(PATTERN_SIGNED)
    timestamp = data[0]
    data = np.array(data[1:])
    data = 1680 * ((data) - data.min()) / (
        data.max() - data.min())
    return timestamp, data


def parse_v3_unsigned_normalized(as_bits):
    data = as_bits.unpack(PATTERN_UNSIGNED)
    timestamp = data[0]
    data = np.array(data[1:])
    data = 1680 * ((data) - data.min()) / (
        data.max() - data.min())
    return timestamp, data


def parse_v4_unsigned_scaled(as_bits):
    data = as_bits.unpack(PATTERN_UNSIGNED)
    timestamp = data[0]
    data = np.array(data[1:])
    data = SIGNAL_SCALE * (np.array(data))
    return timestamp, data

class BleDongleServer(StreamingServer):
    def __init__(self, serial_port, ip=None):
        self.ip = ip
        self.serial_port = serial_port
        self.adapter = pygatt.BGAPIBackend(serial_port=self.serial_port)
        self.device = None
        self.temp_timestamps = np.zeros(5)
        self.temp_data = np.zeros((5, 12))
        self.uuid = str(uuid4())
        self.is_init = False

        info = StreamInfo('Muse', 'EEG', 5, 256, 'float32', self.uuid)

        info.desc().append_child_value("manufacturer", "Muse")
        channels = info.desc().append_child("channels")

        for c in ['TP9', 'AF7', 'AF8', 'TP10', 'Right AUX']:
            channels.append_child("channel") \
                .append_child_value("label", c) \
                .append_child_value("unit", "microvolts") \
                .append_child_value("type", "EEG")
        self.outlet = StreamOutlet(info, 12, 360)

    def find_ip(self):
        devices = self.adapter.scan()
        first_device = next((x for x in devices if 'muse' in x['name'].lower()), None)
        if first_device is None:
            return None
        ip = next((x for x in devices if 'muse' in x['name'].lower()), None)['address']
        logger.info("found device at address:{}. device data: {}".format(ip, first_device))
        return ip

    def is_init(self):
        return self.is_init

    def start(self):
        self.adapter.start()
        if self.ip is None:
            ip = self.find_ip()
            if ip is None:
                message = "could not find ip."
                logger.warning(message)
                raise RuntimeError(message)
            self.ip = ip
        logger.info('server is trying to connect to ip {}'.format(self.ip))
        self.device = self.adapter.connect(self.ip)
        # The 0x000e is the handle of the Client Characteristic Configuration (CCC) uuid 2902
        a = self.device.discover_characteristics()
        self.device.char_write_handle(0x000e, [0x02, 0x64, 0x0a], False)
        all_uuids = []
        for uuid, desc in a.iteritems():
            all_uuids.append("uuid: " + str(desc.uuid) + ", handle:" + str(desc.handle))
        print("found udds: {}".format(all_uuids))
        self.subscribe(self.device)
        self.is_init = True

        while 1:
            try:
                sleep(1)
            except KeyboardInterrupt:
                logger.info("got keyboard in BLE")
                break

    def stop(self):
        if self.device is not None:
            self.device.disconnect()
            self.adapter.stop()

    def measure_response_time(self, num_iteration):
        iterations = np.empty(num_iteration)
        for i in xrange(num_iteration):
            start = datetime.datetime.now()
            a = self.device.get_rssi()
            end = datetime.datetime.now()
            delta = end - start
            iterations[i] = delta.total_seconds() * 1000

        logger.info("time took to receive answer ms - mean: " +
                    str(iterations.mean()) + " std: " + str(iterations.std()) +
                    " min:" + str(iterations.min()) + " max:" + str(iterations.max()))

    def subscribe(self, device):
        # eeg data:
        device.subscribe('273e0003-4c4d-454d-96be-f03bac821358', callback=self.raw_eeg)  # 32 -- 0x20
        device.subscribe('273e0004-4c4d-454d-96be-f03bac821358', callback=self.raw_eeg)  # 35 -- 0x23
        device.subscribe('273e0005-4c4d-454d-96be-f03bac821358', callback=self.raw_eeg)  # 38 -- 0x26
        device.subscribe('273e0006-4c4d-454d-96be-f03bac821358', callback=self.raw_eeg)  # 41 -- 0x29
        device.subscribe('273e0007-4c4d-454d-96be-f03bac821358', callback=self.raw_eeg)  # 44 -- 0x2c

        # dle-ref , 08 characteristic
        # device.subscribe('273e0008-4c4d-454d-96be-f03bac821358',callback=self.handle_drl_ref)  # 17--  0x11

        # battery ,

    #        device.subscribe('273e000b-4c4d-454d-96be-f03bac821358', callback=self.battery_packet)  # 26 -- 0x1A

    # gyrometer data , characteristic 09
    #        device.subscribe('273e0009-4c4d-454d-96be-f03bac821358', callback=self.handle_gyro)  # 20 -- 0x14
    # device.subscribe('273e0002-4c4d-454d-96be-f03bac821358', callback=self.print_data)  # 29 --  # not sent
    # device.subscribe('273e0001-4c4d-454d-96be-f03bac821358', callback=self.print_data)  # 14 --  # not sent
    # device.subscribe('00002a00-0000-1000-8000-00805f9b34fb', callback=self.print_data)  # 7 --
    # device.subscribe('00002a01-0000-1000-8000-00805f9b34fb', callback=self.print_data)  # 9 --
    # device.subscribe('00002a04-0000-1000-8000-00805f9b34fb', callback=self.print_data)  # 1 --
    # device.subscribe('273e000a-4c4d-454d-96be-f03bac821358', callback=self.print_data)  # 23--

    @staticmethod
    def handle_gyro(handle, data):
        try:
            # un packing
            # 160 bits
            aa = bitstring.Bits(bytes=data)
            pattern = "uint:16,uint:12,uint:12,uint:12,uint:12,uint:12,uint:12, \
                   uint:12,uint:12,uint:12,uint:12,uint:12,uint:12"
            res = aa.unpack(pattern)
            x = res[1:5]
            y = res[5:9]
            z = res[9:13]
            logger.info("handle: 0x%x   x: %s y: %s z: %s", handle, str(list(x)), str(list(y)), str(list(z)))
        except Exception as e:
            logger.exception("failed processing handle:0x%x ", handle)

    @staticmethod
    def handle_drl_ref(handle, data):
        try:
            # The Driven Right Leg (DRL) and the Common Mode Sense (CMS) connections correspond to the electrical reference, or "ground", of the system. The CMS is the reference channel, compared to which all the EEG signals are measured. The DRL is responsible for bringing the potential of the subject as close as possible to the "zero" of the electrical system.
            # un packing
            # 160 bits
            aa = bitstring.Bits(bytes=data)
            pattern = "uint:16,uint:16,uint:16,uint:16,uint:16,uint:16,uint:16, \
                uint:16,uint:16,uint:16"
            res = aa.unpack(pattern)
            logger.info("handle: 0x%x   res: %s ", handle, str(list(res)))
        except Exception as e:
            logger.exception("failed processing handle:0x%x ", handle)

    @staticmethod
    def battery_packet(handle, data):
        try:
            # un packing
            aa = bitstring.Bits(bytes=data)
            pattern = "uint:16,uint:16,uint:16,uint:16,uint:16,uint:16,uint:16, \
                uint:16,uint:16,uint:16"
            res = aa.unpack(pattern)
            temp = res[4]  # Temperature in degrees Celsius.
            battery = res[1] / 512  # Charge percentage remaining of battery.
            voltage = res[2] * 2.2  # Millivolts of battery from the view of the fuel gauge.
            logger.info("handle: 0x%x   temp: %s battery %s voltage: %s", handle, str(temp), str(battery), str(voltage))
        except Exception as e:
            logger.exception("failed processing handle:0x%x ", handle)

    def print_data_new(self, handle, data):
        try:
            # un packing
            aa = bitstring.Bits(bytes=data)
            pattern = "uint:16,uint:16,uint:16,uint:16,uint:16,uint:16,uint:16, \
                uint:16,uint:16,uint:16"
            res = aa.unpack(pattern)
            logger.info("handle: 0x%x   data: %s", handle, str(list(res)))
        except Exception as e:
            logger.exception("failed processing handle:0x%x ", handle)

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
            timestamp = current_milli_time()
            as_bits = bitstring.Bits(bytes=data)
            # timestamp, data = parse_v4_unsigned_scaled(as_bits)
            timestamp_npt, data = parse_v4_unsigned_scaled(as_bits)
            index = int((handle - 32) / 3)

            self.temp_data[index] = data
            self.temp_timestamps[index] = timestamp
            # last data received
            if handle == 35:
                # affect as timestamps the first timestamps - 12 sample
                timestamps = np.arange(-12, 0) / 256.
                timestamps += np.min(self.temp_timestamps)
                self.process(self.temp_data, timestamps)
                self._init_sample()
        except Exception as e:
            logger.exception("failed processing handle:0x%x ", handle)

    def _init_sample(self):
        """initialize array to store the samples"""
        self.temp_timestamps = np.zeros(5)
        self.temp_data = np.zeros((5, 12))

    def process(self, data, timestamps):
        for ii in range(12):
            self.outlet.push_sample(data[:, ii], timestamps[ii])

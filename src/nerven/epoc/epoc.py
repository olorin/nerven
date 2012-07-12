from collections import namedtuple, defaultdict, deque
import numpy as np
from epoc_bits import *
import _parse

Gyro = namedtuple('Gyro', ['x', 'y'])

class EpocPacket(object):
    def __init__(self, raw_pkt):
        self.raw = np.array(map(ord,raw_pkt), dtype='int16')
        self.digital = {}
        self.physical = {}
        self.gyro = Gyro(0, 0)

class EpocDevice(object):
    sensors = EPOC_MASK.keys()

    def __init__(self, stream_path="/dev/nervend"):
        self.cur_pkt = None
        self.sensor_q = dict([(s, None) for s in self.sensors])
        self.battery = -1
        self.init_tail()
        self.stream_path = stream_path
        self.stream = open(stream_path, 'rb')
        self.update()

    def update(self):
        pkt = self.stream.read(32)
        self.cur_pkt = self._parse(pkt)
        self.update_tail(self.cur_pkt)

    def update_tail(self, pkt):
        for sensor in self.sensors:
            val = pkt.physical[sensor]
            self.sensor_tail[sensor].append(val)

    def init_tail(self):
        self.sensor_tail = {}
        maxlen = TAIL_LEN * SAMPLE_FREQ
        for sensor in self.sensors:
            self.sensor_tail[sensor] = deque([0.0]*maxlen, maxlen=maxlen)

    def _parse(self, pkt):
        new_pkt = EpocPacket(pkt)
        self.counter = new_pkt.raw[0]
        # if counter byte is a battery update, update battery
        # charge is stored as a percentage 0-100
        if self.counter & 128:
            batt = self.counter & 127
            batt = min(batt, BATTERY_MAX)
            batt = max(batt, BATTERY_MIN)
            batt -= BATTERY_MIN
            batt = int(float(batt)/float(BATTERY_MAX-BATTERY_MIN)*100)
            self.battery = batt
        for sensor, mask in EPOC_MASK.items():
            level = _parse.get_level(new_pkt.raw, mask)
            level -= SENSOR_DIG_MAX
            new_pkt.digital[sensor] = level
            level = float(level)/SENSOR_DIG_MAX*SENSOR_PHYS_MAX
            new_pkt.physical[sensor] = level
            setattr(new_pkt, sensor, level)
        q_sensor = self._get_measured_sensor()
        if q_sensor is not None:
            level = _parse.get_level(new_pkt.raw, QUAL_MASK)
            level = float(level)/QUAL_NORM_FACTOR
            self.sensor_q[q_sensor] = level
        new_pkt.gyro = Gyro(ord(pkt[29]) - GYRO_OFFSET[0], 
                            ord(pkt[30]) - GYRO_OFFSET[1])
        return new_pkt

    def _get_level(self, pkt, mask):
        level = 0
        for i in range(13, -1, -1):
            level <<= 1
            b, o = (mask[i] / 8) + 1, mask[i] % 8
            level |= (ord(pkt[b]) >> o) & 1
        return level

    def _get_measured_sensor(self):
        sensors = SENSOR_QUALITY_ORDER
        c = self.counter
        if c >= 64 and c < 64+14:
            c -= 64
        if c > 15:
            return None
        return sensors[c]
    

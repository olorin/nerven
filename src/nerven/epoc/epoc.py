from collections import namedtuple, defaultdict, deque
import numpy as np
from epoc_bits import *
try:
    import _parse
    cython_exts = True
except ImportError:
    cython_exts = False

Gyro = namedtuple('Gyro', ['x', 'y'])

class EpocPacket(object):
    def __init__(self, raw_pkt):
        self.raw = np.array(map(ord,raw_pkt), dtype='int16')
        self.digital = {}
        self.physical = {}
        self.gyro = Gyro(0, 0)

class BaseDevice(object):
    sensors = EPOC_MASK.keys()

    def __init__(self, stream_path="/dev/nervend"):
        self.cur_pkt = None
        self.sensor_q = dict([(s, None) for s in self.sensors])
        self.battery = -1
        if cython_exts:
            self.get_level = _parse.get_level
        else:
            self.get_level = self._get_level
        self.init_tail()
        self.stream_path = stream_path
        self.init_stream()
        self.update()

    def update(self):
        pkt = self.read_data()
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
            level = self.get_level(new_pkt.raw, mask)
            level -= SENSOR_DIG_MAX
            new_pkt.digital[sensor] = level
            level = float(level)/SENSOR_DIG_MAX*SENSOR_PHYS_MAX
            new_pkt.physical[sensor] = level
            setattr(new_pkt, sensor, level)
        q_sensor = self._get_measured_sensor()
        if q_sensor is not None:
            level = self.get_level(new_pkt.raw, QUAL_MASK)
            level = float(level)/QUAL_NORM_FACTOR
            self.sensor_q[q_sensor] = level
        new_pkt.gyro = Gyro(ord(pkt[29]) - GYRO_OFFSET[0], 
                            ord(pkt[30]) - GYRO_OFFSET[1])
        return new_pkt

    def _get_level(self, pkt, mask):
        pkt = map(chr, pkt)
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

class EpocDevice(BaseDevice):
    def init_stream(self):
        self.stream = open(self.stream_path, 'rb')

    def read_data(self):
        pkt = self.stream.read(PKT_SIZE)
        if len(pkt) != PKT_SIZE:
            print("warning: don't have a full packet, only read %d bytes." % len(pkt))
        return pkt

class ZeroDevice(BaseDevice):
    def init_stream(self):
        self.stream = open('/dev/zero', 'rb')

    def read_data(self):
        return ''.join(['\0']*PKT_SIZE)

    def _parse(self, pkt):
        new_pkt = EpocPacket(pkt)
        self.counter = 0
        self.battery = 0
        for sensor,mask in EPOC_MASK.items():
            setattr(new_pkt, sensor, 0)
            new_pkt.digital[sensor] = 0
            new_pkt.physical[sensor] = 0.0
            self.sensor_q[sensor] = 0.0
        new_pkt.gyro = Gyro(0,0)
        return new_pkt

        
    

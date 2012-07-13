from datetime import datetime
from consts import *


class EpocWriter(object):
    '''Abstract class.'''
    def __init__(self, outpath, epoc):
        self.path = outpath
        self.start_time = datetime.now()

    def write_packet(self, pkt):
        pass

    def close(self):
        pass

    def running(self):
        return datetime.now() - self.start_time

class RawWriter(EpocWriter):
    '''Just dumps the raw EPOC packets to disk.'''
    def __init__(self, outpath, epoc):
        EpocWriter.__init__(self, outpath, epoc)
        self.stream = open(outpath, 'wb')

    def write_packet(self, pkt):
        buf = map(chr, pkt.raw)
        self.stream.write(''.join(buf))

    def close(self):
        self.stream.close()
        

    

        


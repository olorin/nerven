import numpy as np
cimport numpy as np

def get_level(np.ndarray[np.int16_t,ndim=1] pkt, mask):
    cdef level = 0
    cdef int b,o
    for i in range(13, -1, -1):
        level <<= 1
        b = (mask[i]/8)+1
        o = mask[i] % 8
        level |= (pkt[b] >> o) & 1
    return level

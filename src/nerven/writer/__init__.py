from writers import *

have_edf = False
try:
    from edflib import _edflib as edf
    have_edf = True
    from EdfWriter import EdfWriter
except ImportError:
    print("Can't find edflib, EDF output disabled.")

backends = {
    'raw' : RawWriter,
    }

if have_edf:
    backends['edf'] = EdfWriter

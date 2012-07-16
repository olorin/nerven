from collections import namedtuple
import wx

from exceptions import *

ConfigOption = namedtuple('ConfigOption', ['description', 'type', 'default'])

class NervenConfig(object):
    options = {
            'data_path' : ConfigOption('Path to EPOC raw data', 'string', '/dev/nervend'),
            'normalize_brainwaves' : ConfigOption('Normalize brain wave power', 'bool', False),
            }

    def __init__(self, create=False, cfg=None):
        self.cfg = cfg
        if self.cfg is None:
            self.cfg = wx.Config('nerven')

        self.getters = {
                'string' : lambda k: self.cfg.Read(k),
                'float' : lambda k: self.cfg.ReadFloat(k),
                'int' : lambda k: self.cfg.ReadInt(k),
                'bool' : lambda k: self.cfg.ReadBool(k),
                }

        self.setters = {
                'string' : lambda k,v: self.cfg.Write(k,v),
                'float' : lambda k,v: self.cfg.WriteFloat(k,v),
                'int' : lambda k,v: self.cfg.WriteInt(k,v),
                'bool' : lambda k,v: self.cfg.WriteBool(k,v),
                }

        if create:
            for k in self.options:
                if not self.cfg.Exists(k):
                    self.set(k, self.options[k].default)

    def get(self, key):
        if key not in self.options.keys():
            raise OptionDoesNotExist(key)
        return self.getters[self.options[key].type](key)

    def set(self, key, val):
        if key not in self.options.keys():
            raise OptionDoesNotExist(key)
        return self.setters[self.options[key].type](key, val)

    def write(self):
        return self.cfg.Flush()

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, val):
        return self.set(key, val)



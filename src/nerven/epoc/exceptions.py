class NervenError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return 'NervenError: %s' % str(self.msg)

class NotImplementedError(NervenError):
    pass

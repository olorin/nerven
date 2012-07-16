class NervenException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return 'NervenException: %s' % self.msg

class OptionDoesNotExist(NervenException):
    def __repr__(self):
        return 'Config option %s does not exist.' % self.msg

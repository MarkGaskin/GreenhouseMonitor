import pickle
from Messages.Message import Message


class SysLogMessage(Message):
    def __init__(self, level, log):
        self.name = "SysLog"
        self.level = level
        self.log = log

    def encode(self):
        msg = {"name": self.name,
               "level": self.level,
               "log": self.log}
        return pickle.dumps(msg)


def parseSysLogMessage(encodedMsg):
    msg = pickle.loads(encodedMsg)
    return SysLogMessage(msg["level"], msg["log"])

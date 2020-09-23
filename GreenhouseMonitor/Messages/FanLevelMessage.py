import pickle
from Messages.Message import Message


class FanLevelMessage(Message):
    def __init__(self, fanLevel):
        self.name = "FanLevel"
        self.fanLevel = fanLevel

    def encode(self):
        msg = {"name": self.name,
               "fanLevel": self.fanLevel
               }
        return pickle.dumps(msg)


def parseFanLevelMessage(encodedMsg):
    msg = pickle.loads(encodedMsg)
    return FanLevelMessage(msg["fanLevel"])

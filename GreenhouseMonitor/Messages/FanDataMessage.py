import pickle
from Messages.Message import Message


class FanDataMessage(Message):
    def __init__(self, fanOn):
        self.name = "FanData"
        self.fanOn = fanOn

    def encode(self):
        msg = {"name": self.name,
               "fanOn": self.fanOn
               }
        return pickle.dumps(msg)


def parseFanDataMessage(encodedMsg):
    msg = pickle.loads(encodedMsg)
    return FanDataMessage(msg["fanOn"])
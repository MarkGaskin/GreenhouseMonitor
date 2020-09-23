import pickle
from Messages.Message import Message


class UpdateFanLevelMessage(Message):
    def __init__(self, fanLevel):
        self.name = "UpdateFanLevel"
        self.fanLevel = fanLevel

    def encode(self):
        msg = {"name": self.name,
               "fanLevel": self.fanLevel
               }
        return pickle.dumps(msg)


def parseUpdateFanLevelMessage(encodedMsg):
    msg = pickle.loads(encodedMsg)
    return UpdateFanLevelMessage(msg["fanLevel"])
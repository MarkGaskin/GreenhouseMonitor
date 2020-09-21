import pickle
from Messages.Message import Message


class LightDataMessage(Message):
    def __init__(self, lightOn):
        self.name = "LightData"
        self.lightOn = lightOn

    def encode(self):
        msg = {"name": self.name,
               "lightOn": self.lightOn
               }
        return pickle.dumps(msg)


def parseLightDataMessage(encodedMsg):
    msg = pickle.loads(encodedMsg)
    return LightDataMessage(msg["lightOn"])
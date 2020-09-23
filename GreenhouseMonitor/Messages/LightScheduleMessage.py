import pickle
from Messages.Message import Message


class LightScheduleMessage(Message):
    def __init__(self, lightOn, lightOff):
        self.name = "LightSchedule"
        self.lightOn = lightOn
        self.lightOff = lightOff

    def encode(self):
        msg = {"name": self.name,
               "lightOn": self.lightOn,
               "lightOff": self.lightOff
               }
        return pickle.dumps(msg)


def parseLightScheduleMessage(encodedMsg):
    msg = pickle.loads(encodedMsg)
    return LightScheduleMessage(msg["lightOn"], msg["lightOff"])
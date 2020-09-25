import pickle
from Messages.Message import Message


class TriggerClimateDataMessage(Message):
    def __init__(self, triggerTemperature, triggerHumidity):
        self.name = "TriggerClimateData"
        self.triggerTemperature = triggerTemperature
        self.triggerHumidity = triggerHumidity

    def encode(self):
        msg = {"name": self.name,
               "triggerTemperature": self.triggerTemperature,
               "triggerHumidity":  self.triggerHumidity
               }
        return pickle.dumps(msg)


def parseTriggerClimateDataMessage(encodedMsg):
    msg = pickle.loads(encodedMsg)
    return TriggerClimateDataMessage(msg["triggerTemperature"], msg["triggerHumidity"])
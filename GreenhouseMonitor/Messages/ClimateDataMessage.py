import pickle
from Messages.Message import Message


class ClimateDataMessage(Message):
    def __init__(self, climateData):
        self.name = "ClimateData"
        self.climateData = climateData

    def encode(self):
        msg = {"name": self.name,
               "climateData": self.climateData
               }
        return pickle.dumps(msg)


def parseClimateDataMessage(encodedMsg):
    msg = pickle.loads(encodedMsg)
    return ClimateDataMessage(msg["climateData"])
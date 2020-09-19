import pickle
from Messages.Message import Message


class DataLogMessage(Message):
    def __init__(self, temp, humidity, fanOn, lightOn):
        self.name = "DataLog"
        self.temp = temp
        self.humidity = humidity
        self.fanOn = fanOn
        self.lightOn = lightOn

    def encode(self):
        msg = {"name": self.name,
               "temp": self.temp,
               "humidity": self.humidity,
               "fanOn": self.fanOn,
               "lightOn": self.lightOn
               }
        return pickle.dumps(msg)


def parseDataLogMessage(encodedMsg):
    msg = pickle.loads(encodedMsg)
    return DataLogMessage(msg["temp"], msg["humidity"], msg["fanOn"], msg["lightOn"])

import pickle
from Messages.Message import Message


class EnvironmentDataMessage(Message):
    def __init__(self, envData):
        self.name = "EnvironmentData"
        self.environmentData = envData

    def encode(self):
        msg = {"name": self.name,
               "environmentData": self.environmentData
               }
        return pickle.dumps(msg)


def parseEnvironmentDataMessage(encodedMsg):
    msg = pickle.loads(encodedMsg)
    return EnvironmentDataMessage(msg["environmentData"])

import pickle
from Messages.Message import Message


class UpdateLightMessage(Message):
    def __init__(self, lightOn):
        self.name = "UpdateLight"
        self.lightOn = lightOn

    def encode(self):
        msg = {"name": self.name,
               "lightOn": self.lightOn
               }
        return pickle.dumps(msg)


def parseUpdateLightMessage(encodedMsg):
    msg = pickle.loads(encodedMsg)
    return UpdateLightMessage(msg["lightOn"])
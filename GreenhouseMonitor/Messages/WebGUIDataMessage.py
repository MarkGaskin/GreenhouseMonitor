import pickle
from Messages.Message import Message


class WebGUIDataMessage(Message):
    def __init__(self, webGUIData):
        self.name = "WebGUIData"
        self.webGUIData = webGUIData

    def encode(self):
        msg = {"name": self.name,
               "webGUIData": self.webGUIData
               }
        return pickle.dumps(msg)


def parseWebGUIDataMessage(encodedMsg):
    msg = pickle.loads(encodedMsg)
    return WebGUIDataMessage(msg["webGUIData"])

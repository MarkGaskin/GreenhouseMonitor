import pickle
from Messages.Message import Message


class ActorAddressMessage(Message):
    def __init__(self, webGUIAddr, envCtrlAddr, loggingAddr):
        self.name = "ActorAddress"
        self.webGUIAddr = webGUIAddr
        self.envCtrlAddr = envCtrlAddr
        self.loggingAddr = loggingAddr

    def encode(self):
        msg = {"name": self.name,
               "webGUIAddr": self.webGUIAddr,
               "envCtrlAddr": self.envCtrlAddr,
               "loggingAddr": self.loggingAddr}
        return pickle.dumps(msg)


def parseActorAddressMessage(encodedMsg):
    msg = pickle.loads(encodedMsg)
    return ActorAddressMessage(msg["webGUIAddr"], msg["envCtrlAddr"], msg["loggingAddr"])

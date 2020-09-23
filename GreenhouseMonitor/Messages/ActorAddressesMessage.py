import pickle
from Messages.Message import Message


class ActorAddressMessage(Message):
    def __init__(self, webGUIAddr, envCtrlAddr, logActAddr):
        self.name = "ActorAddress"
        self.webGUIAddr = webGUIAddr
        self.envCtrlAddr = envCtrlAddr
        self.logActAddr = logActAddr

    def encode(self):
        msg = {"name": self.name,
               "webGUIAddr": self.webGUIAddr,
               "envCtrlAddr": self.envCtrlAddr,
               "logActAddr": self.logActAddr}
        return pickle.dumps(msg)


def parseActorAddressMessage(encodedMsg):
    msg = pickle.loads(encodedMsg)
    return ActorAddressMessage(msg["webGUIAddr"], msg["envCtrlAddr"], msg["logActAddr"])

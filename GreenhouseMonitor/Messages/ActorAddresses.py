import pickle
from Messages.Message import Message


class ActorAddressMessage(Message):
    def __init__(self, webGUIAddr, envCtrlAddr, LogActAddr):
        self.name = "ActorAddress"
        self.webGUIAddr = webGUIAddr
        self.envCtrlAddr = envCtrlAddr
        self.LogActAddr = LogActAddr

    def encode(self):
        msg = {"name": self.name,
               "webGUIAddr": self.webGUIAddr,
               "envCtrlAddr": self.envCtrlAddr,
               "LogActAddr": self.LogActAddr}
        return pickle.dumps(msg)


def parseActorAddressMessage(encodedMsg):
    msg = pickle.loads(encodedMsg)
    return ActorAddressMessage(msg["webGUIAddr"], msg["envCtrlAddr"], msg["LogActAddr"])

from thespian.actors import Actor
from Messages.ActorAddresses import parseActorAddressMessage
from Messages.Message import parseMessage
from Actors.EnvironmentController import EnvironmentData
import datetime


class WebGUIData:
    def __init__(self, envData):
        self.envData = envData
        self.time = datetime.datetime.now()


class WebGUI(Actor):
    def __init__(self, *args, **kwargs):
        print("WebGUI is alive")
        self.count = 0
        self.logActAddr = ""
        self.envCtrlAddr = ""
        super().__init__(*args, **kwargs)

    def receiveMessage(self, message, sender):
        msg = parseMessage(message)
        if message == "getStatus":
            self.count = self.count + 1
            climateData = ClimateData
            self.send(sender, WebGUIData())
        elif msg.name == "ActorAddress":
            msg = parseActorAddressMessage(message)
            self.logActAddr = msg.logActAddr
            self.envCtrlAddr = msg.envCtrlAddr
            self.schedActAddr = msg.schedActAddr
        else:
            self.send(sender, "Blank")


from thespian.actors import Actor
from Actors.BaseActor import BaseActor
from Messages.ActorAddressesMessage import parseActorAddressMessage
from Messages.Message import parseMessage
from Actors.EnvironmentController import EnvironmentData
from Actors.EnvironmentActors.ClimateReader import ClimateData
from Messages.EnvironmentDataMessage import parseEnvironmentDataMessage
from Messages.WebGUIDataMessage import WebGUIDataMessage
import datetime


class WebGUIData:
    def __init__(self, envData=EnvironmentData(ClimateData(0, 0), False, False)):
        self.envData = envData
        self.time = datetime.datetime.now()


class WebGUI(BaseActor):
    def __init__(self, *args, **kwargs):
        print("WebGUI is alive")
        self.count = 0
        self.logActAddr = ""
        self.envCtrlAddr = ""
        self.schedActAddr = ""
        self.webGUIData = WebGUIData()
        super().__init__(*args, **kwargs)

    def receiveMessage(self, message, sender):
        msg = parseMessage(message)
        if msg.name == "getData":
            print("getData hit")
            webGUIDataMessage = WebGUIDataMessage(self.webGUIData)
            self.send(sender, webGUIDataMessage.encode())
        elif msg.name == "ActorAddress":
            print("AA updated for scheduling Actors")
            msg = parseActorAddressMessage(message)
            self.logActAddr = msg.logActAddr
            self.envCtrlAddr = msg.envCtrlAddr
            self.schedActAddr = msg.schedActAddr
        elif msg.name == "EnvironmentData":
            msg = parseEnvironmentDataMessage(message)
            self.webGUIData.envData = msg.environmentData
            self.webGUIData.time = datetime.datetime.now()
        else:
            self.send(sender, "Blank")


from Messages.ActorAddresses import parseActorAddressMessage
from .LoggingActor import *
from Actors.EnvironmentActors.FanController import FanController
from Actors.EnvironmentActors.ClimateReader import ClimateReader
from Actors.EnvironmentActors.LightController import LightController


class EnvironmentController(Actor):
    def __init__(self, *args, **kwargs):
        self.FanCtrlAddr = ""
        self.LightCtrlAddr = ""
        self.ClimRdrAddr = ""
        self.LogActAddr = ""
        self.webGUIAddr = ""
        print("EnvironmentController is alive")
        super().__init__(*args, **kwargs)

    def receiveMessage(self, message, sender):
        msg = parseMessage(message)
        if msg.name == "Launch":
            self.FanCtrlAddr = self.createActor(FanController)
            self.ClimRdrAddr = self.createActor(ClimateReader)
            self.LightCtrlAddr = self.createActor(LightController)
        elif msg.name == "ActorAddress":
            msg = parseActorAddressMessage(message)
            self.LogActAddr = msg.LogActAddr
            self.webGUIAddr = msg.webGUIAddr
            print("AA hit")
        else:
            return

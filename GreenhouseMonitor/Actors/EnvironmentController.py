from Messages.Message import parseMessage
from Messages.ActorAddresses import parseActorAddressMessage
from .LoggingActor import *
from Actors.EnvironmentActors.FanController import FanController
from Actors.EnvironmentActors.ClimateReader import ClimateReader, ClimateData
from Actors.EnvironmentActors.LightController import LightController


class EnvironmentData:
    def __init__(self, climateData, lightOn, fanOn):
        self.climateData = climateData
        self.lightOn = lightOn
        self.fanOn = fanOn


class EnvironmentController(Actor):
    def __init__(self, *args, **kwargs):
        self.FanCtrlAddr = ""
        self.LightCtrlAddr = ""
        self.ClimRdrAddr = ""
        self.LogActAddr = ""
        self.webGUIAddr = ""
        self.schedActAddr = ""
        self.envData = EnvironmentData(ClimateData(21, 52), True, False)
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
            self.LogActAddr = msg.logActAddr
            self.webGUIAddr = msg.webGUIAddr
            self.schedActAddr = msg.schedActAddr
        elif msg.name == "GetEnvironmentData":
            return self.send(self.webGUIAddr, "SendClimateData")
        else:
            return

from Messages.Message import parseMessage, Message
from Messages.ActorAddressesMessage import parseActorAddressMessage
from .LoggingActor import *
from Actors.EnvironmentActors.FanController import FanController
from Actors.EnvironmentActors.ClimateReader import ClimateReader, ClimateData
from Actors.EnvironmentActors.LightController import LightController
from Messages.EnvironmentDataMessage import EnvironmentDataMessage
from Messages.ClimateDataMessage import parseClimateDataMessage
from Messages.FanDataMessage import parseFanDataMessage
from Messages.LightDataMessage import parseLightDataMessage
from Actors.BaseActor import BaseActor


class EnvironmentData:
    def __init__(self, climateData = ClimateData(), lightOn = False, fanOn = False):
        self.climateData = climateData
        self.lightOn = lightOn
        self.fanOn = fanOn


class EnvironmentController(BaseActor):
    def __init__(self, *args, **kwargs):
        self.fanCtrlAddr = ""
        self.climRdrAddr = ""
        self.lightCtrlAddr = ""
        self.logActAddr = ""
        self.webGUIAddr = ""
        self.schedActAddr = ""
        self.envData = EnvironmentData()
        print("EnvironmentController is alive")
        super().__init__(*args, **kwargs)

    def receiveMessage(self, message, sender):
        msg = parseMessage(message)
        if msg.name == "ActorAddress":
            msg = parseActorAddressMessage(message)
            self.logActAddr = msg.logActAddr
            self.webGUIAddr = msg.webGUIAddr
            self.schedActAddr = msg.schedActAddr
        elif msg.name == "Launch":
            self.fanCtrlAddr = self.createActor(FanController)
            self.climRdrAddr = self.createActor(ClimateReader)
            self.lightCtrlAddr = self.createActor(LightController)
        elif msg.name == "StartEnvironmentTasks":
            fanCtrlMessage = Message("UpdateFanStatus")
            self.scheduleMsg(self.fanCtrlAddr, fanCtrlMessage.encode(), 30)

            lightCtrlMessage = Message("UpdateLightStatus")
            self.scheduleMsg(self.lightCtrlAddr, lightCtrlMessage.encode(), 300)

            climRdrMessage = Message("UpdateClimateStatus")
            self.scheduleMsg(self.climRdrAddr, climRdrMessage.encode(), 100)

            environmentDataMsg = Message("UpdateEnvironmentData")
            self.scheduleMsg(self.myAddress, environmentDataMsg.encode(), 300)
        elif msg.name == "ClimateData":
            msg = parseClimateDataMessage(message)
            self.envData.climateData = msg.climateData
        elif msg.name == "FanData":
            msg = parseFanDataMessage(message)
            self.envData.fanOn = msg.fanOn
        elif msg.name == "LightData":
            msg = parseLightDataMessage(message)
            self.envData.lightOn = msg.lightOn
        elif msg.name == "UpdateEnvironmentData":
            msg = EnvironmentDataMessage(self.envData)
            self.send(self.webGUIAddr, msg.encode())
            self.send(self.logActAddr, msg.encode())
        else:
            return

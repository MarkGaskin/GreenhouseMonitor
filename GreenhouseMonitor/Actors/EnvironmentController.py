from Messages.Message import parseMessage, Message
from Messages.ActorAddressesMessage import parseActorAddressMessage
from .LoggingActor import *
from Actors.EnvironmentActors.FanController import FanController
from Actors.EnvironmentActors.ClimateReader import ClimateReader, ClimateData
from Actors.EnvironmentActors.LightController import LightController
from Messages.EnvironmentDataMessage import EnvironmentDataMessage
from Messages.ClimateDataMessage import parseClimateDataMessage
from Messages.FanLevelMessage import parseFanLevelMessage
from Messages.LightDataMessage import parseLightDataMessage
from Messages.LightScheduleMessage import parseLightScheduleMessage, LightScheduleMessage
from Actors.BaseActor import BaseActor
import logging
import time

logger = logging.getLogger(__name__)


class EnvironmentData:
    def __init__(self, climateData=ClimateData(), lightOn=False, fanLevel=2):
        self.climateData = climateData
        self.lightOn = lightOn
        self.fanLevel = fanLevel


class LightSchedule:
    def __init__(self, currentOn=datetime.datetime.min, currentOff=datetime.datetime.max,
                 upcomingOn=datetime.datetime.min, upcomingOff=datetime.datetime.max):
        self.currentOn = currentOn
        self.currentOff = currentOff
        self.upcomingOn = upcomingOn
        self. upcomingOff = upcomingOff


class EnvironmentController(BaseActor):
    def __init__(self, *args, **kwargs):
        self.fanCtrlAddr = ""
        self.climRdrAddr = ""
        self.lightCtrlAddr = ""
        self.loggingAddr = ""
        self.webGUIAddr = ""
        self.lightSchedule = LightSchedule()
        self.envData = EnvironmentData()
        print("EnvironmentController is alive")
        super().__init__(*args, **kwargs)

    def receiveMessage(self, message, sender):
        msg = parseMessage(message)
        if msg.name == "ActorAddress":
            msg = parseActorAddressMessage(message)
            self.loggingAddr = msg.loggingAddr
            self.webGUIAddr = msg.webGUIAddr
        elif msg.name == "Launch":
            self.fanCtrlAddr = self.createActor(FanController)
            self.climRdrAddr = self.createActor(ClimateReader)
            self.lightCtrlAddr = self.createActor(LightController)
        elif msg.name == "StartEnvironmentTasks":
            fanCtrlMessage = Message("UpdateFanStatus")
            self.scheduleMsg(self.fanCtrlAddr, fanCtrlMessage.encode(), 30)

            lightCtrlMessage = Message("UpdateLightStatus")
            self.scheduleMsg(self.lightCtrlAddr, lightCtrlMessage.encode(), 30)

            climRdrMessage = Message("UpdateClimateStatus")
            self.scheduleMsg(self.climRdrAddr, climRdrMessage.encode(), 30)

            environmentDataMsg = Message("UpdateEnvironmentData")
            self.scheduleMsg(self.myAddress, environmentDataMsg.encode(), 30)
        elif msg.name == "ClimateData":
            msg = parseClimateDataMessage(message)
            self.logInfo("Environment Received Climate Temp, Humidity : " + str(msg.climateData.temperature) + ", " + str(msg.climateData.humidity))
            self.envData.climateData = msg.climateData
        elif msg.name == "FanLevel":
            msg = parseFanLevelMessage(message)
            print("Environment Received Fan Level : " + str(msg.fanLevel))
            self.logInfo("Environment Received Fan Level : " + str(msg.fanLevel))
            self.envData.fanLevel = msg.fanLevel
        elif msg.name == "LightData":
            msg = parseLightDataMessage(message)
            self.envData.lightOn = msg.lightOn
        elif msg.name == "UpdateEnvironmentData":
            msg = EnvironmentDataMessage(self.envData)
            self.send(self.webGUIAddr, msg.encode())
            self.send(self.loggingAddr, msg.encode())
        elif msg.name == "LightScheduleComplete":
            self.logInfo("LightScheduleComplete")
            self.send(self.webGUIAddr, message)
            replyMsg = LightScheduleMessage(self.lightSchedule.upcomingOn, self.lightSchedule.upcomingOff)
            self.send(self.lightCtrlAddr, replyMsg.encode())
        elif msg.name == "LightScheduleStarted":
            self.logInfo("LightScheduleStarted")
        elif msg.name == "LightSchedule":
            msg = parseLightScheduleMessage(message)
            self.lightSchedule.currentOn = msg.lightOn[0]
            self.lightSchedule.currentOff = msg.lightOff[0]
            self.lightSchedule.upcomingOn = msg.lightOn[1]
            self.lightSchedule.upcomingOff = msg.lightOff[1]
            fwMsg = LightScheduleMessage(self.lightSchedule.currentOn, self.lightSchedule.currentOff)
            self.send(self.lightCtrlAddr, fwMsg.encode())
        elif msg.name == "UpdateLight":
            self.send(self.lightCtrlAddr, message)
        elif msg.name == "UpdateFanLevel":
            self.send(self.fanCtrlAddr, message)
        else:
            return

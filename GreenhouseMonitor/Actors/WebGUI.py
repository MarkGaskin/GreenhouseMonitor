from thespian.actors import Actor
from Actors.BaseActor import BaseActor
from Messages.ActorAddressesMessage import parseActorAddressMessage
from Messages.Message import parseMessage
from Actors.EnvironmentController import EnvironmentData, LightSchedule
from Messages.UpdateFanLevelMessage import parseUpdateFanLevelMessage
from Messages.EnvironmentDataMessage import parseEnvironmentDataMessage
from Messages.LightScheduleMessage import LightScheduleMessage, parseLightScheduleMessage
from Messages.UpdateLightMessage import UpdateLightMessage
from Messages.WebGUIDataMessage import WebGUIDataMessage
import datetime
import logging


logger = logging.getLogger(__name__)


class WebGUIData:
    def __init__(self, envData=EnvironmentData(), lightSchedule=LightSchedule()):
        self.envData = envData
        self.lightSchedule = lightSchedule
        self.time = datetime.datetime.now()


class WebGUI(BaseActor):
    def __init__(self, *args, **kwargs):
        print("WebGUI is alive")
        self.count = 0
        self.logActAddr = ""
        self.envCtrlAddr = ""
        self.webGUIData = WebGUIData()
        super().__init__(*args, **kwargs)

    def receiveMessage(self, message, sender):
        msg = parseMessage(message)
        if msg.name == "getData":
            webGUIDataMessage = WebGUIDataMessage(self.webGUIData)
            self.send(sender, webGUIDataMessage.encode())
        elif msg.name == "ActorAddress":
            msg = parseActorAddressMessage(message)
            self.logActAddr = msg.logActAddr
            self.envCtrlAddr = msg.envCtrlAddr
        elif msg.name == "EnvironmentData":
            msg = parseEnvironmentDataMessage(message)
            self.webGUIData.envData = msg.environmentData
            self.webGUIData.time = datetime.datetime.now()
        elif msg.name == "LightScheduleComplete":
            self.webGUIData.lightSchedule.currentOn = self.webGUIData.lightSchedule.upcomingOn
            self.webGUIData.lightSchedule.currentOff = self.webGUIData.lightSchedule.upcomingOff
            replyMsg = LightScheduleMessage([self.webGUIData.lightSchedule.currentOn, self.webGUIData.lightSchedule.upcomingOn],
                                            [self.webGUIData.lightSchedule.currentOff, self.webGUIData.lightSchedule.upcomingOff])
            self.send(self.envCtrlAddr, replyMsg.encode())
        elif msg.name == "LightSchedule":
            msg = parseLightScheduleMessage(message)
            self.webGUIData.lightSchedule.currentOn = msg.lightOn[0]
            self.webGUIData.lightSchedule.currentOff = msg.lightOff[0]
            self.webGUIData.lightSchedule.upcomingOn = msg.lightOn[1]
            self.webGUIData.lightSchedule.upcomingOff = msg.lightOff[1]
            print(msg.lightOn[0])
            print(msg.lightOff[0])
            print(msg.lightOn[1])
            print(msg.lightOff[1])
            self.send(self.envCtrlAddr, message)
            return
        elif msg.name == "UpdateFanLevel":
            msg = parseUpdateFanLevelMessage(message)
            self.webGUIData.envData.fanLevel = msg.fanLevel
            self.send(self.envCtrlAddr, message)
        elif msg.name == "ToggleLightStatus":
            self.webGUIData.envData.lightOn = not self.webGUIData.envData.lightOn
            self.send(self.envCtrlAddr, UpdateLightMessage(self.webGUIData.envData.lightOn).encode())
        else:
            self.send(sender, "Blank")


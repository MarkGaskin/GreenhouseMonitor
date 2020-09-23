from thespian.actors import Actor
from Messages.Message import parseMessage, Message
from Messages.LightDataMessage import LightDataMessage
from Messages.LightScheduleMessage import parseLightScheduleMessage
from Messages.UpdateLightMessage import parseUpdateLightMessage
import datetime
import logging


logger = logging.getLogger(__name__)


def isTimeBetween(begin_time, end_time):
    # If check time is not given, default to current UTC time
    check_time = datetime.datetime.now()
    if begin_time < end_time:
        return begin_time <= check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time


def updateLightStatus(lightStatus):
    return lightStatus


class LightController(Actor):
    def __init__(self, *args, **kwargs):
        print("LightController is alive")
        self.lightOn = False
        self.scheduledOn = False
        self.onTime = datetime.datetime.min
        self.offTime = datetime.datetime.max
        super().__init__(*args, **kwargs)

    def receiveMessage(self, message, sender):
        msg = parseMessage(message)
        if msg.name == "UpdateLightStatus":
            scheduledOn = isTimeBetween(self.onTime, self.offTime)
            print("Scheduled On: " + str(scheduledOn))
            print(self.lightOn)
            print(self.onTime)
            print(self.offTime)
            if self.scheduledOn != scheduledOn:
                print("Changing light status to " + str(scheduledOn))
                msgName = "LightScheduleStarted" if scheduledOn else "LightScheduleComplete"
                self.send(sender, Message(msgName).encode())
                self.lightOn = updateLightStatus(scheduledOn)
            self.scheduledOn = scheduledOn
            self.send(sender, LightDataMessage(self.lightOn).encode())

        elif msg.name == "LightSchedule":
            msg = parseLightScheduleMessage(message)
            self.onTime = msg.lightOn
            self.offTime = msg.lightOff

        elif msg.name == "UpdateLight":
            msg = parseUpdateLightMessage(message)
            self.lightOn = updateLightStatus(msg.lightOn)


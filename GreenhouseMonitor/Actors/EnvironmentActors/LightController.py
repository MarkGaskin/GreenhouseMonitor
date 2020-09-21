from thespian.actors import Actor
from Messages.Message import parseMessage
from Messages.LightDataMessage import LightDataMessage
import datetime


def isTimeBetween(begin_time, end_time):
    # If check time is not given, default to current UTC time
    check_time = datetime.datetime.now()
    if begin_time < end_time:
        return begin_time <= check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time


def updateLightStatus(lightStatus):
    return


class LightController(Actor):
    def __init__(self, *args, **kwargs):
        print("LightController is alive")
        self.lightOn = False
        self.onTime = datetime.datetime.now()
        self.offTime = datetime.datetime.now()
        super().__init__(*args, **kwargs)

    def receiveMessage(self, message, sender):
        msg = parseMessage(message)
        if msg.name == "UpdateLightStatus":
            desiredOn = isTimeBetween(self.onTime, self.offTime)
            if self.lightOn != desiredOn:
                updateLightStatus(desiredOn)
            else:
                return
            self.send(sender, LightDataMessage(desiredOn).encode())

        return

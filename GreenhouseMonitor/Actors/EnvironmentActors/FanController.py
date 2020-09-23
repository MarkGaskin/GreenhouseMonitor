from thespian.actors import Actor
from Messages.Message import parseMessage
from Messages.FanLevelMessage import FanLevelMessage
from Messages.UpdateFanLevelMessage import parseUpdateFanLevelMessage
import logging


logger = logging.getLogger(__name__)


totalDuration = 5


def updateFanStatus(fanStatus):
    return fanStatus


class FanController(Actor):
    def __init__(self, *args, **kwargs):
        print("FanController is alive")
        self.count = 0
        self.fanOn = False
        self.fanLevel = 2
        super().__init__(*args, **kwargs)

    def receiveMessage(self, message, sender):
        msg = parseMessage(message)
        if msg.name == "UpdateFanStatus":
            if self.count == 0 or self.count == self.fanLevel:
                print("Changing Fan Status to " + str(self.count == 0))
                self.fanOn = updateFanStatus(self.count == 0)

            self.count += 1
            self.send(sender, FanLevelMessage(self.fanLevel).encode())
            if self.count > totalDuration:
                self.count = 0
        elif msg.name == "UpdateFanLevel":
            msg = parseUpdateFanLevelMessage(message)
            print("Fan Received Update Fan Level : " + str(msg.fanLevel))
            if msg.fanLevel >= 5:
                self.fanLevel = 5
            elif msg.fanLevel <= 1:
                self.fanLevel = 1
            else:
                self.fanLevel = msg.fanLevel
        else:
            return

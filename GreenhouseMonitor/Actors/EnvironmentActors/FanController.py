from thespian.actors import Actor
from Messages.Message import parseMessage
from Messages.FanDataMessage import FanDataMessage


fanDuration = 6

def updateFanStatus(fanStatus):
    return

class FanController(Actor):
    def __init__(self, *args, **kwargs):
        print("FanController is alive")
        self.count = 0
        self.fanOn = False
        self.onDuration = 2
        self.offDuration = fanDuration - self.onDuration
        super().__init__(*args, **kwargs)

    def receiveMessage(self, message, sender):
        msg = parseMessage(message)
        if msg.name == "UpdateFanStatus":
            if (self.fanOn and (self.count > self.onDuration)) or (not self.fanOn and (self.count > self.offDuration)):
                updateFanStatus(not self.fanOn)
                self.fanOn = not self.fanOn
                self.count = 0
            else:
                self.count += 1
            self.send(sender, FanDataMessage(self.fanOn).encode())
        else:
            return

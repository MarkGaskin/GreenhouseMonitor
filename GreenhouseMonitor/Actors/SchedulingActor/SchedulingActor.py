from thespian.actors import Actor
from Messages.ActorAddressesMessage import parseActorAddressMessage
from Messages.Message import parseMessage
from crontab import CronTab
import os
import pickle


class SchedulingActor(Actor):
    def __init__(self, *args, **kwargs):
        print("WebGUI is alive")
        self.count = 0
        self.logActAddr = ""
        self.envCtrlAddr = ""
        self.webGUIAddr = ""
        print("SchedulingActor is alive")
        super().__init__(*args, **kwargs)

    def receiveMessage(self, message, sender):
        msg = parseMessage(message)
        if msg.name == "ActorAddress":
            msg = parseActorAddressMessage(message)
            self.logActAddr = msg.logActAddr
            self.envCtrlAddr = msg.envCtrlAddr
            self.webGUIAddr = msg.webGUIAddr
        elif msg.name == "ScheduleTask":
            print("Scheduling")
            scriptDir = os.path.dirname(__file__)  # absolute dir the script is in
            addr = {'addr': self.logActAddr}
            command = "python3 " + scriptDir + "\\SendSysLog.py " + str(pickle.dumps(addr))
            print(command)
            cron = CronTab(tab=("""* * * * * """ + command))
            cron.write()
        else:
            self.send(sender, "Blank")


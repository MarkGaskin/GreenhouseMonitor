from thespian.actors import *
from Actors.BaseActor import BaseActor
from Messages.ActorAddressesMessage import parseActorAddressMessage
from Messages.Message import parseMessage, Message
from crontab import CronTab
import os
import pickle


class SchedulingActor(BaseActor):
    def __init__(self, *args, **kwargs):
        print("WebGUI is alive")
        self.count = 0
        self.logActAddr = ""
        self.envCtrlAddr = ""
        self.webGUIAddr = ""
        self.username = "SchedulingActor"
        print("SchedulingActor is alive")
        super().__init__(*args, **kwargs)

    def receiveMessage(self, message, sender):
        msg = parseMessage(message)
        if msg.name == "ActorAddress":
            msg = parseActorAddressMessage(message)
            self.logActAddr = msg.logActAddr
            self.envCtrlAddr = msg.envCtrlAddr
            self.webGUIAddr = msg.webGUIAddr
        elif msg.name == "ScheduleTasks":
            #print("Scheduling")
            #scriptDir = os.path.dirname(__file__)  # absolute dir the script is in
            #addr = {'addr': self.logActAddr}
            #command = "python3 " + scriptDir + "/SendSysLog.py " + str(addr)
            #print(command)
            ## cron = CronTab(tab=("""* * * * * """ + command))
            #cron = CronTab(user=True)
            #job = cron.new(command=command, comment="SendSysLog")
            #job.minute.every(1)
            # cron.write()
            return

        elif msg.name == "TimingTask1":
            print("TimingTask1 has been called")
            msg = Message("SendEnvironmentData")
            self.send(self.envCtrlAddr, msg.encode())
        else:
            self.send(sender, "Blank")


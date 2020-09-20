#!/bin/python3

from Messages.SysLogMessage import SysLogMessage
from thespian.actors import *
import sys
import pickle

print("SendSysLog script")
msg = SysLogMessage("INFO", "CRON is alive!!!")
addr = pickle.loads(sys.arg1)
ActorSystem().tell(addr, msg.encode())
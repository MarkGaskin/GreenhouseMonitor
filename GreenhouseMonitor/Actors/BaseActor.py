from thespian.actors import Actor
from abc import abstractmethod
import _thread
import time
from Messages.SysLogMessage import SysLogMessage

class BaseActor(Actor):
    def __init__(self, *args, **kwargs):
        self.loggingAddr = ""
        super().__init__(*args, **kwargs)

    def finiteSend(self, targetAddr, msg, delay, iterations):
        i = 0
        while i < iterations:
            self.send(targetAddr, msg)
            time.sleep(delay)
            i = i + 1

    def infiniteSend(self, targetAddr, msg, delay):
        while True:
            self.send(targetAddr, msg)
            time.sleep(delay)

    def scheduleMsg(self, targetAddr, msg, delay, iterations=0):
        if iterations == 0:
            _thread.start_new_thread(self.infiniteSend, (targetAddr, msg, delay))
        else:
            _thread.start_new_thread(self.finiteSend, (targetAddr, msg, delay, iterations))

    def logInfo(self, log):
        if self.loggingAddr != "":
            self.send(self.loggingAddr, SysLogMessage("Info", log).encode())
        else:
            print("Attempted to log before logging address was known")

    def logWarning(self, log):
        if self.loggingAddr != "":
            self.send(self.loggingAddr, SysLogMessage("Warning", log).encode())
        else:
            print("Attempted to log before logging address was known")

    def logError(self, log):
        if self.loggingAddr != "":
            self.send(self.loggingAddr, SysLogMessage("Error", log).encode())
        else:
            print("Attempted to log before logging address was known")

    def logDebug(self, log):
        if self.loggingAddr != "":
            self.send(self.loggingAddr, SysLogMessage("Debug", log).encode())
        else:
            print("Attempted to log before logging address was known")

    @abstractmethod
    def receiveMessage(self, msg, sender):
        return


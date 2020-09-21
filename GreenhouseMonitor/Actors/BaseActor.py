from thespian.actors import Actor
from abc import abstractmethod
import _thread
import time


# class ScheduleMessage(threading.Thread):
#    def __init__(self, targetAddr, msg, delay, iterations):
#        threading.Thread.__init__(self)
#        self.targetAddr = targetAddr
#        self.msg = msg
#        self.delay = delay
#        self.iterations = iterations#
#
#   def run(self):
#       while self.iterations > 0:
#           self.send(self.targetAddr, self.msg)
#           time.sleep(self.delay)
#           self.iterations = self.iterations - 1

class BaseActor(Actor):
    def __init__(self, *args, **kwargs):
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

    @abstractmethod
    def receiveMessage(self, msg, sender):
        return


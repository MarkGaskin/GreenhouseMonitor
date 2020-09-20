from thespian.actors import Actor
from Messages.Message import parseMessage


class FanController(Actor):
    def __init__(self, *args, **kwargs):
        print("FanController is alive")
        super().__init__(*args, **kwargs)

    def receiveMessage(self, message, sender):
        msg = parseMessage(message)
        if msg.name == "GetTempAndHumidity":
            temperature = getTemperature()
            humidity = getHumidity()
            return ClimateData(temperature, humidity)
        else:
            return

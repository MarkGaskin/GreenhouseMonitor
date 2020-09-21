from thespian.actors import Actor
from Messages.Message import parseMessage
from Messages.ClimateDataMessage import ClimateDataMessage


class ClimateData:
    def __init__(self, temperature=0, humidity=0):
        self.temperature = temperature
        self.humidity = humidity


def getTemperature():
    return 21.1


def getHumidity():
    return 53.0


class ClimateReader(Actor):
    def __init__(self, *args, **kwargs):
        print("ClimateController is alive")
        super().__init__(*args, **kwargs)

    def receiveMessage(self, message, sender):
        msg = parseMessage(message)
        if msg.name == "UpdateClimateStatus":
            climateData = ClimateData(getTemperature(), getHumidity())
            self.send(sender, ClimateDataMessage(climateData).encode())
        else:
            return

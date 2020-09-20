from thespian.actors import Actor


class ClimateData:
    def __init__(self, temperature, humidity):
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
        return

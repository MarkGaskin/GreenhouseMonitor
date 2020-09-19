from thespian.actors import Actor


class ClimateReader(Actor):
    def __init__(self, *args, **kwargs):
        print("ClimateController is alive")
        super().__init__(*args, **kwargs)

    def receiveMessage(self, message, sender):
        return

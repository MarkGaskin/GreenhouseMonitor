from thespian.actors import Actor


class LightController(Actor):
    def __init__(self, *args, **kwargs):
        print("LightController is alive")
        self.lightOn = False
        super().__init__(*args, **kwargs)

    def receiveMessage(self, message, sender):
        return

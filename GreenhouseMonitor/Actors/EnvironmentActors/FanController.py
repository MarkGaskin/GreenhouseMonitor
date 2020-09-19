from thespian.actors import Actor


class FanController(Actor):
    def __init__(self, *args, **kwargs):
        print("FanController is alive")
        super().__init__(*args, **kwargs)

    def receiveMessage(self, message, sender):
        return

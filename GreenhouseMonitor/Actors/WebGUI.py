from thespian.actors import Actor


class WebGUI(Actor):
    def __init__(self, *args, **kwargs):
        print("WebGUI is alive")
        super().__init__(*args, **kwargs)

    def receiveMessage(self, message, sender):
        return


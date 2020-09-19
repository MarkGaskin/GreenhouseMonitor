from thespian.actors import Actor


class WebGUI(Actor):
    def __init__(self, *args, **kwargs):
        print("WebGUI is alive")
        self.count = 0
        super().__init__(*args, **kwargs)

    def receiveMessage(self, message, sender):
        if message == "getStatus":
            self.count = self.count + 1
            self.send(sender, str(self.count))
        else:
            self.send(sender, "Blank")


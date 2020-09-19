from thespian.actors import Actor

class Hello(Actor):
    def receiveMessage(self, message, sender):
        self.send(sender, "Hello, World!")

import pickle


class Message:
    def __init__(self, name):
        self.name = name

    def encode(self):
        msg = {"name": self.name}
        return pickle.dumps(msg)


def parseMessage(encodedMsg):
    msg = pickle.loads(encodedMsg)
    return Message(msg["name"])

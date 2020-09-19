from thespian.actors import *
from Actors.LoggingActor import LoggingActor
from Actors.EnvironmentController import EnvironmentController
from Actors.WebGUI import WebGUI
import sys
from flask import Flask
from Messages.Message import Message
from Messages.SysLogMessage import SysLogMessage
from Messages.DataLogMessage import DataLogMessage
from Messages.ActorAddresses import ActorAddressMessage
import socket


def get_my_ip():
    """Return the ipaddress of the local host"""
    return socket.gethostbyname(socket.gethostname())


app = Flask(__name__)


@app.route('/')
def hello():
    returnVal = ActorSystem().ask(aSys.createActor(WebGUI, globalName='WebGUISingleton'), "getStatus", 60)
    return returnVal, 200


if __name__ == "__main__":
    # if "shutdown" in sys.argv:
    #    ActorSystem('multiprocQueueBase').shutdown()
    #    sys.exit(0)
    # asys = ActorSystem('simpleSystemBase')
    # Setup this system as the convention leader, and give it a capability "Server"
    # Note by default actor systems use port 1900, so we'll set this here too
    capabilities = {"Convention Address.IPv4": (get_my_ip(), 1900), "Server": True}
    aSys = ActorSystem("multiprocTCPBase", capabilities)

    webGUI = aSys.createActor(WebGUI, globalName='WebGUISingleton')
    loggingActor = aSys.createActor(LoggingActor)
    envCtrl = aSys.createActor(EnvironmentController)

    launchMsg = Message("Launch")
    ActorSystem().tell(envCtrl, launchMsg.encode())

    msg = SysLogMessage("INFO", "System launched")
    ActorSystem().tell(loggingActor, msg.encode())

    msg = DataLogMessage(21, 53, True, True)
    ActorSystem().tell(loggingActor, msg.encode())

    actorAddrMsg = ActorAddressMessage(webGUI, envCtrl, loggingActor)
    ActorSystem().tell(envCtrl, actorAddrMsg.encode())

    app.run()

    aSys.shutdown()



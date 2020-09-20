from thespian.actors import *
from Actors.LoggingActor import LoggingActor
from Actors.EnvironmentController import EnvironmentController
from Actors.SchedulingActor.SchedulingActor import SchedulingActor
from Actors.WebGUI import WebGUI
from flask import Flask, render_template
from Messages.Message import Message
from Messages.SysLogMessage import SysLogMessage
from Messages.DataLogMessage import DataLogMessage
from Messages.ActorAddresses import ActorAddressMessage
import socket
import templates


def get_my_ip():
    """Return the ipaddress of the local host"""
    return socket.gethostbyname(socket.gethostname())


app = Flask(__name__)


@app.route('/')
def hello():
    statusMsg = Message("getData")
    webGUIData = ActorSystem().ask(aSys.createActor(WebGUI, globalName='WebGUISingleton'), statusMsg.encode(), 60)
    return render_template("homepage.html", webGUIData)


if __name__ == "__main__":
    # if "shutdown" in sys.argv:
    #    ActorSystem('multiprocQueueBase').shutdown()
    #    sys.exit(0)
    # asys = ActorSystem('simpleSystemBase')
    # Setup this system as the convention leader, and give it a capability "Server"
    # Note by default actor systems use port 1900, so we'll set this here too
    # capabilities = {"Convention Address.IPv4": (get_my_ip(), 1900)}
    # aSys = ActorSystem("multiprocTCPBase", capabilities)

    aSys = ActorSystem('simpleSystemBase')

    webGUI = aSys.createActor(WebGUI, globalName='WebGUISingleton')
    loggingActor = aSys.createActor(LoggingActor)
    envCtrl = aSys.createActor(EnvironmentController)
    schedActor = aSys.createActor(SchedulingActor)

    launchMsg = Message("Launch")
    ActorSystem().tell(envCtrl, launchMsg.encode())

    msg = SysLogMessage("INFO", "System launched")
    ActorSystem().tell(loggingActor, msg.encode())

    msg = DataLogMessage(21, 53, True, True)
    ActorSystem().tell(loggingActor, msg.encode())

    actorAddrMsg = ActorAddressMessage(webGUI, envCtrl, loggingActor, schedActor)
    ActorSystem().tell(webGUI, actorAddrMsg.encode())
    ActorSystem().tell(envCtrl, actorAddrMsg.encode())
    ActorSystem().tell(loggingActor, actorAddrMsg.encode())
    ActorSystem().tell(schedActor, actorAddrMsg.encode())

    msg = Message("ScheduleTask")
    # ActorSystem().tell(schedActor, msg.encode())

    app.run()




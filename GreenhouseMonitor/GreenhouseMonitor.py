from thespian.actors import *
from Actors.LoggingActor import LoggingActor
from Actors.EnvironmentController import EnvironmentController
from Actors.WebGUI import WebGUI
import sys
from flask import Flask

app = Flask(__name__)


if __name__ == "__main__":
    # if "shutdown" in sys.argv:
    #    ActorSystem('multiprocQueueBase').shutdown()
    #    sys.exit(0)
    # asys = ActorSystem('simpleSystemBase')
    asys = ActorSystem('multiprocTCPBase')

    webGUI = asys.createActor(WebGUI)
    loggingActor = asys.createActor(LoggingActor)
    envCtrl = asys.createActor(EnvironmentController)
    ActorSystem().tell(loggingActor, "SysLog")
    ActorSystem().tell(loggingActor, "DataABCD")
    ActorSystem().tell(envCtrl, "Launch")

    asys.shutdown()


@app.route('/')
def hello():
    ActorSystem().tell()
    return "Hello World!"

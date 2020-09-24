from thespian.actors import *
from Actors.LoggingActor import LoggingActor
from Actors.EnvironmentController import EnvironmentController
from Actors.SchedulingActor.SchedulingActor import SchedulingActor
from Actors.WebGUI import WebGUI
from flask import Flask, render_template, request, redirect
from Messages.Message import Message
from Messages.SysLogMessage import SysLogMessage
from Messages.DataLogMessage import DataLogMessage
from Messages.ActorAddressesMessage import ActorAddressMessage
from Messages.WebGUIDataMessage import parseWebGUIDataMessage
from Messages.LightScheduleMessage import LightScheduleMessage
from Messages.UpdateFanLevelMessage import UpdateFanLevelMessage
from Messages.UpdateLightMessage import UpdateLightMessage
import socket
import datetime


def getTimes(onString, offString, date):
    if onString is not "" and offString is not "":
        dateString = datetime.datetime.strftime(date, "%x ")
        timeOn = datetime.datetime.strptime(dateString + onString, "%x %H:%M")
        timeOff = datetime.datetime.strptime(dateString + offString, "%x %H:%M")
        if timeOn >= timeOff:
            timeOff += datetime.timedelta(days=1)
        if timeOff < datetime.datetime.now():
            timeOn += datetime.timedelta(days=1)
            timeOff += datetime.timedelta(days=1)
        return timeOn, timeOff
    else:
        return datetime.datetime.min, datetime.datetime.max


def get_my_ip():
    """Return the ipaddress of the local host"""
    return socket.gethostbyname(socket.gethostname())


app = Flask(__name__)


@app.route('/')
def homepage():
    statusMsg = Message("getData")
    webGUIData = parseWebGUIDataMessage(ActorSystem().ask(aSys.createActor(WebGUI, globalName='WebGUISingleton'),
                                                          statusMsg.encode(),
                                                          60))
    templateData = {
        'time': webGUIData.webGUIData.time,
        'envData': webGUIData.webGUIData.envData,
        'lightStatus': "ON" if webGUIData.webGUIData.envData.lightOn else "OFF",
        'currentOn': datetime.datetime.strftime(webGUIData.webGUIData.lightSchedule.currentOn, "%H:%M"),
        'currentOff': datetime.datetime.strftime(webGUIData.webGUIData.lightSchedule.currentOff, "%H:%M"),
        'upcomingOn': datetime.datetime.strftime(webGUIData.webGUIData.lightSchedule.upcomingOn, "%H:%M"),
        'upcomingOff': datetime.datetime.strftime(webGUIData.webGUIData.lightSchedule.upcomingOff, "%H:%M")
    }

    return render_template("homepage.html", **templateData)


@app.route('/UpdateSchedule', methods=['POST'])
def SubmitSchedule():
    currentOn, currentOff = getTimes(request.form['CurrentStartTime'],
                                     request.form['CurrentEndTime'],
                                     datetime.datetime.now())
    upcomingOn, upcomingOff = getTimes(request.form['UpcomingStartTime'],
                                       request.form['UpcomingEndTime'],
                                       datetime.datetime.now() + datetime.timedelta(days=1))
    webGUI = ActorSystem().createActor(WebGUI, globalName='WebGUISingleton')
    ActorSystem().ask(webGUI, LightScheduleMessage([currentOn, upcomingOn], [currentOff, upcomingOff]).encode(),10)
    return redirect('/')


@app.route('/UpdateFanLevel', methods=['POST'])
def UpdateFanLevel():
    fanLevel = int(request.form['FanLevel'])
    print(fanLevel)
    webGUI = ActorSystem().createActor(WebGUI, globalName='WebGUISingleton')
    ActorSystem().tell(webGUI, UpdateFanLevelMessage(fanLevel).encode())
    return redirect('/')


@app.route('/ToggleLightStatus', methods=['POST'])
def ToggleLightStatus():
    webGUI = ActorSystem().createActor(WebGUI, globalName='WebGUISingleton')
    ActorSystem().tell(webGUI, Message("ToggleLightStatus").encode())
    return redirect('/')


if __name__ == "__main__":
    # if "shutdown" in sys.argv:
    #    ActorSystem('multiprocQueueBase').shutdown()
    #    sys.exit(0)
    # asys = ActorSystem('simpleSystemBase')
    # Setup this system as the convention leader, and give it a capability "Server"
    # Note by default actor systems use port 1900, so we'll set this here too
    # capabilities = {"Convention Address.IPv4": (get_my_ip(), 1900)}
    # aSys = ActorSystem("multiprocTCPBase", capabilities)

    # aSys = ActorSystem('simpleSystemBase')

    aSys = ActorSystem('multiprocQueueBase')

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
    ActorSystem().tell(webGUI, actorAddrMsg.encode())
    ActorSystem().tell(envCtrl, actorAddrMsg.encode())
    ActorSystem().tell(loggingActor, actorAddrMsg.encode())

    msg = Message("StartEnvironmentTasks")
    ActorSystem().tell(envCtrl, msg.encode())

    app.run()




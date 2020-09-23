from thespian.actors import Actor
from Actors.BaseActor import BaseActor
from Messages.Message import parseMessage
from Messages.SysLogMessage import parseSysLogMessage
from Messages.EnvironmentDataMessage import parseEnvironmentDataMessage
from Messages.ActorAddressesMessage import parseActorAddressMessage
import os
import csv
import datetime
import logging


scriptDir = os.path.dirname(__file__)  # absolute dir the script is in
relDataLogPath = "../../dataLog.csv"
absDataLogFilePath = os.path.join(scriptDir, relDataLogPath)
relSysLogPath = "../../sysLog.csv"
absSysLogFilePath = os.path.join(scriptDir, relSysLogPath)

sysLogFieldNames = ['dateString', 'timeString', 'Level', 'Log']
dataLogFieldNames = ['dateString', 'timeString', 'Temperature', 'Humidity', 'LightOn', 'FanLevel']


class LoggingActor(BaseActor):
    def __init__(self, *args, **kwargs):
        self.absDataLogFilePath = absDataLogFilePath
        self.webGUIAddr = ""
        self.envCtrlAddr = ""

        filename = "SystemLog_" + datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d_%H_%M") + ".log"
        filepath = os.path.join("Logging", filename)
        if not os.path.isdir("Logging"):
            os.makedirs("Logging")
        logging.basicConfig(filename=filepath, filemode='w',
                            format='%(name)s - %(asctime)s - %(levelname)s - %(message)s')

        print("LoggingActor is alive")
        super().__init__(*args, **kwargs)

    def receiveMessage(self, message, sender):
        msg = parseMessage(message)
        if msg.name == "ActorAddress":
            msg = parseActorAddressMessage(message)
            self.webGUIAddr = msg.webGUIAddr
            self.envCtrlAddr = msg.envCtrlAddr
        elif msg.name == "SysLog":
            msg = parseSysLogMessage(message)
            if msg.level == "Info":
                logging.info(msg.log)
            elif msg.level == "Error":
                logging.error(msg.log)
            else:
                logging.debug(msg.log)
        elif msg.name == "EnvironmentData":
            msg = parseEnvironmentDataMessage(message)
            with open(self.absDataLogFilePath, 'a+', newline='') as csvFile:
                csvWriter = csv.DictWriter(csvFile, fieldnames=dataLogFieldNames)
                time = datetime.datetime.now()
                dateString = time.strftime("%Y-%m-%d")
                timeString = time.strftime("%X")
                csvWriter.writerow({'dateString': dateString,
                                    'timeString': timeString,
                                    'Temperature': msg.environmentData.climateData.temperature,
                                    'Humidity': msg.environmentData.climateData.humidity,
                                    'LightOn': msg.environmentData.lightOn,
                                    'FanLevel': msg.environmentData.fanLevel})
        else:
            return

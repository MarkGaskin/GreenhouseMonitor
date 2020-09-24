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
from logging.handlers import TimedRotatingFileHandler
import sys


scriptDir = os.path.dirname(__file__)  # absolute dir the script is in
relDataLogPath = "../../dataLog.csv"
absDataLogFilePath = os.path.join(scriptDir, relDataLogPath)
dataLogFieldNames = ['dateString', 'timeString', 'Temperature', 'Humidity', 'LightOn', 'FanLevel']

FORMATTER = logging.Formatter("%(asctime)s — %(levelname)s — %(message)s")
LOG_FILE = "SystemLog_" + datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d_%H_%M") + ".log"
try:
    os.mkdir("Logging")
except FileExistsError:
    pass
filePath = os.path.join("Logging", LOG_FILE)


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = TimedRotatingFileHandler(filePath, when='midnight')
    file_handler.setFormatter(FORMATTER)
    return file_handler


class LoggingActor(BaseActor):
    def __init__(self, *args, **kwargs):
        self.absDataLogFilePath = absDataLogFilePath
        self.webGUIAddr = ""
        self.envCtrlAddr = ""

        file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
        file_handler.setFormatter(FORMATTER)

        self.logger = logging.getLogger("LoggingActor")
        self.logger.addHandler(get_file_handler())
        self.logger.addHandler(get_console_handler())
        self.logger.propagate = False
        self.logger.info("System launched")
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
                self.logger.info(msg.log)
            elif msg.level == "Error":
                self.logger.error(msg.log)
            elif msg.level == "Debug":
                self.logger.debug(msg.log)
            else:
                self.logger.warning(msg.log)
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

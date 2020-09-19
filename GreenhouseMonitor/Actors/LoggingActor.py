from thespian.actors import Actor
from Messages.Message import parseMessage
from Messages.SysLogMessage import parseSysLogMessage
from Messages.DataLogMessage import parseDataLogMessage
import os
import csv
import datetime


scriptDir = os.path.dirname(__file__)  # absolute dir the script is in
relDataLogPath = "../../dataLog.csv"
absDataLogFilePath = os.path.join(scriptDir, relDataLogPath)
relSysLogPath = "../../sysLog.csv"
absSysLogFilePath = os.path.join(scriptDir, relSysLogPath)

sysLogFieldNames = ['dateString', 'timeString', 'Level', 'Log']
dataLogFieldNames = ['dateString', 'timeString', 'Temperature', 'Humidity', 'LightOn', 'FanOn']


class LoggingActor(Actor):
    def __init__(self, *args, **kwargs):
        self.absDataLogFilePath = absDataLogFilePath
        self.absSysLogFilePath = absSysLogFilePath
        print("LoggingActor is alive")
        super().__init__(*args, **kwargs)

    def receiveMessage(self, message, sender):
        msg = parseMessage(message)
        if msg.name == "SysLog":
            msg = parseSysLogMessage(message)
            with open(self.absSysLogFilePath, 'a+', newline='') as csvFile:
                csvWriter = csv.DictWriter(csvFile, fieldnames=sysLogFieldNames)
                time = datetime.datetime.now()
                dateString = time.strftime("%Y-%m-%d")
                timeString = time.strftime("%X")
                csvWriter.writerow({'dateString': dateString,
                                    'timeString': timeString,
                                    'Level': msg.level,
                                    'Log': msg.log})
        elif msg.name == "DataLog":
            msg = parseDataLogMessage(message)
            with open(self.absDataLogFilePath, 'a+', newline='') as csvFile:
                csvWriter = csv.DictWriter(csvFile, fieldnames=dataLogFieldNames)
                time = datetime.datetime.now()
                dateString = time.strftime("%Y-%m-%d")
                timeString = time.strftime("%X")
                csvWriter.writerow({'dateString': dateString,
                                    'timeString': timeString,
                                    'Temperature': msg.temp,
                                    'Humidity': msg.humidity,
                                    'LightOn': msg.lightOn,
                                    'FanOn': msg.fanOn})

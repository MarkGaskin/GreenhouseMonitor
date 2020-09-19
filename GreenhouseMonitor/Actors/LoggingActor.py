from thespian.actors import Actor
import os
import string
import csv
import datetime
import json


scriptDir = os.path.dirname(__file__) # absolute dir the script is in
relDataLogPath = "../../dataLog.csv"
absDataLogFilePath = os.path.join(scriptDir, relDataLogPath)
relSysLogPath = "../../sysLog.csv"
absSysLogFilePath = os.path.join(scriptDir, relSysLogPath)

sysLogFieldNames = ['dateString', 'timeString', 'Level', 'Log']
dataLogFieldNames = ['dateString', 'timeString', 'Temperature', 'Humidity', 'Light']


class LoggingActor(Actor):
    def __init__(self, *args, **kwargs):
        self.absDataLogFilePath = absDataLogFilePath
        self.absSysLogFilePath = absSysLogFilePath
        super().__init__(*args, **kwargs)

    def receiveMessage(self, message, sender):
        if message.startswith("Sys"):
            with open(self.absSysLogFilePath, 'w', newline='') as csvfile:
                spamWriter = csv.DictWriter(csvfile, fieldnames=sysLogFieldNames)
                time = datetime.datetime.now()
                dateString = time.strftime("%Y-%m-%d")
                timeString = time.strftime("%X")
                spamWriter.writerow({'dateString': dateString, 'timeString': timeString, 'Level': 'Warning', 'Log': "Test"})
        elif message.startswith("Data"):
            with open(self.absDataLogFilePath, 'w', newline='') as csvfile:
                print(message[4:])
                spamWriter = csv.DictWriter(csvfile, fieldnames=dataLogFieldNames)
                time = datetime.datetime.now()
                dateString = time.strftime("%Y-%m-%d")
                timeString = time.strftime("%X")
                spamWriter.writerow({'dateString': dateString, 'timeString': timeString, 'Temperature': "0.0", 'Humidity': "0.0", 'Light': "0.0"})
        


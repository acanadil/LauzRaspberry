from azure.iot.device import IoTHubDeviceClient, Message
from datetime import datetime
import json
import Machine
from multiprocessing import Process
import time

CONNECTION_STRING = "HostName=ra-develop-bobstconnect-01.azure-devices.net;DeviceId=LAUZHACKPI1;SharedAccessKey=YXBIJtM6Pp4m4VumdPJjxXJqXLnCpjJFxAIoTMQBSV8="

class DataStream:

    def __init__(self, machine):
        self.client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
        self.client.connect()
        self.input = 0
        self.output = 0
        self.totalOutput = 0
        self.machineState = machine

    def sendTelemetry(self):
        p = Process(target=self._sendTelemetryLoop)
        p.start()

    def _sendTelemetryLoop(self):
        while True:
            self._sendTelemetry()  
    
    def _sendTelemetry(self):
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.') + str(int(datetime.utcnow().microsecond / 1000)).zfill(3) + 'Z'

        data = {
            "telemetry" : {
                "machineid": self.machineState.id,
                "datasource": "172.20.2.5:80",
                "timestamp": timestamp,
                "machinespeed" : self.machineState.speed,
                "totaloutputunitcount" : self.machineState.totalOutput
            }
        }

        json_data = json.dumps(data)
        message = Message(json_data)
        message.content_type = "application/json"
        message.content_encoding = "utf-8"
        message.custom_properties["messageType"] = "Telemetry"
        self.client.send_message(message)
    
    def startJob(self, jobName):
        if self.machineState.jobStarted:
            return
        self.machineState.jobStarted = not self.machineState.jobStarted
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.') + str(int(datetime.utcnow().microsecond / 1000)).zfill(3) + 'Z'
        self.machineState.jobs.append(jobName)
        data = {
            "timestamp" : timestamp,
            "type": "newJob",
            "equipmentId": self.machineState.id,
            "jobId": len(self.machineState.jobs),
            "jobName": jobName,
        }

        json_data = json.dumps([data])
        message = Message(json_data)
        message.content_type = "application/json"
        message.content_encoding = "utf-8"
        message.custom_properties["messageType"] = "MachineEvent"
        self.client.send_message(message)

    def endJob(self, jobName):
        if not self.machineState.jobStarted:
            return
        self.machineState.jobStarted = not self.machineState.jobStarted
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.') + str(int(datetime.utcnow().microsecond / 1000)).zfill(3) + 'Z'
        self.machineState.jobs.append(jobName)
        data = {
            "timestamp" : timestamp,
            "type": "endJob",
            "equipmentId": self.machineState.id,
            "jobId": len(self.machineState.jobs),
            "jobName": jobName,
        }

        json_data = json.dumps([data])        
        message = Message(json_data)
        message.content_type = "application/json"
        message.content_encoding = "utf-8"
        message.custom_properties["messageType"] = "MachineEvent"
        self.client.send_message(message)

    def startProcessing(self, jobName):
        if self.machineState.processStarted:
            return
        self.machineState.processStarted = not self.machineState.processStarted
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.') + str(int(datetime.utcnow().microsecond / 1000)).zfill(3) + 'Z'
        self.machineState.jobs.append(jobName)
        data = {
            "timestamp" : timestamp,
            "type": "endJob",
            "equipmentId": self.machineState.id,
            "jobId": len(self.machineState.jobs),
            "jobName": jobName,
        }

        json_data = json.dumps([data])
        message = Message(json_data)
        message.content_type = "application/json"
        message.content_encoding = "utf-8"
        message.custom_properties["messageType"] = "MachineEvent"
        self.client.send_message(message)

    def stopProcessing(self, jobName):
        if not self.machineState.processStarted:
            return
        self.machineState.processStarted = not self.machineState.processStarted
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.') + str(int(datetime.utcnow().microsecond / 1000)).zfill(3) + 'Z'
        self.machineState.jobs.append(jobName)
        data = {
            "timestamp" : timestamp,
            "type": "endJob",
            "equipmentId": self.machineState.id,
            "jobId": len(self.machineState.jobs),
            "jobName": jobName,
        }

        json_data = json.dumps([data])
        message = Message(json_data)
        message.content_type = "application/json"
        message.content_encoding = "utf-8"
        message.custom_properties["messageType"] = "MachineEvent"
        self.client.send_message(message)
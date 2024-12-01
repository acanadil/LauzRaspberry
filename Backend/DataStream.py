from azure.iot.device import IoTHubDeviceClient, Message
from datetime import datetime
import json
import Machine
from threading import Thread
import time, logging

CONNECTION_STRING = "HostName=ra-develop-bobstconnect-01.azure-devices.net;DeviceId=LAUZHACKPI1;SharedAccessKey=YXBIJtM6Pp4m4VumdPJjxXJqXLnCpjJFxAIoTMQBSV8="

class DataStream:

    def __init__(self, machine):
        self.client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
        self.client.connect()
        self.input = 0
        self.output = 0
        self.totalOutput = 0
        self.machineState = machine
        self.p = None
        self.stop = False
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

    def newInputBox(self):
        self.input += 1
    
    def newOutputBox(self):
        self.output += 1
        self.totalOutput += 1
        self.machineState.totalOutput += 1

    def changeSpeed(self, speed):
        self.machineState.speed = speed
    
    def sendTelemetry(self):
        self.p = Thread(target=self._sendTelemetryLoop)
        self.p.start()

    def increaseEnergy(self, energy):
        self.machineState.energy += energy

    def _sendTelemetryLoop(self):
        while not self.stop:
            self._sendTelemetryCore()
            time.sleep(10)  

    def _sendTelemetryCore(self):
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.') + str(int(datetime.utcnow().microsecond / 1000)).zfill(3) + 'Z'

        data = {
            "telemetry" : {
                "machineid": self.machineState.id,
                "datasource": "172.20.2.5:80",
                "timestamp": timestamp,
                "machinespeed" : self.machineState.speed,
                "totaloutputunitcount" : self.totalOutput,
                "totalworkingenergy": self.machineState.energy
            }
        }

        json_data = json.dumps(data)
        message = Message(json_data)
        self.logger.info(json_data)
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
        if not self.machineState.jobStarted or self.machineState.processStarted:
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
        if self.machineState.processStarted or not self.machineState.jobStarted:
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
        self.input = 0
        self.output = 0

    def stopTelemetry(self):
        self.stop = True
        self.p.join()
    def disconnect(self):
        self.client.disconnect()
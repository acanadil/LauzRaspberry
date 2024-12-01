from flask import Flask
from datetime import datetime
from azure.iot.device import IoTHubDeviceClient, Message

app = Flask(__name__)

currentIP = ""

dict = {
    "machineid": "ThisDoesnotWork",
    "datasource": currentIP,
    "timestamp": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.') + str(int(datetime.utcnow().microsecond / 1000)).zfill(3) + 'Z',
    "machinespeed" : 30,
    "totaloutputunitcount" : 0,
    "cpuload": {
        "Value": 20.139233,
        "Timestamp": "2024-11-30T15:35:34.647Z"
    },
    "mainmachinecycle": {
        "Value": 7,
        "Timestamp": "2024-11-30T15:30:51.437Z"
    },
}

#engine class or variables?
started = False
max_speed = 100
min_speed = 20

@app.route("/engine/increase-speed")
def hello_world():
    return "Speed increased"

@app.route("/engine/decrease-speed")
def hello_world():
    return "Speed decreased"

@app.route("/engine/start")
def hello_world():
    if started:
        return "Engine is already started"
    else:
        return "Engine started"

@app.route("/engine/stop")
def hello_world():
    if not started:
        return "Engine is already stopped"
    else:
        return "Engine stopped"
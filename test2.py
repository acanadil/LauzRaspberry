from Machine import Machine
from DataStream import DataStream

import random, time

id = "lauzhack-pi1"
myMachine = Machine(id)

dataStream = DataStream(myMachine)
dataStream.machineState.speed = 0.75
for _ in range(10):
    dataStream.newInputBox()
    dataStream.newOutputBox()
    time.sleep(0.1)

dataStream.sendTelemetry()
time.sleep(1)
dataStream.machineState.speed = 0.25
time.sleep(2)
#dataStream.stopProcessing()
dataStream.disconnect()
print("TERMINATE!")


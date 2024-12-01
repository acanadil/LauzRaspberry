from Machine import Machine
from DataStream import DataStream

import random, time

id = "lauzhack-pi1"
myMachine = Machine(id)

dataStream = DataStream(myMachine)
dataStream.changeSpeed(0.5)

dataStream.startJob(id)
dataStream.startProcessing(id)
dataStream.sendTelemetry()

sleep_time = 1

counter = 0

print("WHILE")
while counter <= 2000:
    print("IT: ", counter)
    speedChange = random.uniform(0, 1)
    if (round(speedChange)):
        if (speedChange >= 0.75):
            dataStream.changeSpeed(dataStream.machineState.speed + 0.1)
            sleep_time = max(0.1, sleep_time - 0.1)
        else:
            dataStream.changeSpeed(max (0.1, dataStream.machineState.speed - 0.1))
            sleep_time += 0.1
    dataStream.increaseEnergy(speedChange*5 + 0.5)
    dataStream.newInputBox()
    outputBox = round(random.uniform(0.33, 1))
    if (outputBox):
        dataStream.newOutputBox()    
    time.sleep(sleep_time)
    counter  += 1

time.sleep(1)
dataStream.machineState.speed = 0.25
time.sleep(2)
time.sleep(300)
dataStream.stopProcessing(id)
dataStream.stopTelemetry()
dataStream.endJob(id)
dataStream.disconnect()
print("TERMINATE!")


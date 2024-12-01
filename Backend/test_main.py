from Machine import Machine
from DataStream import DataStream

import random, time


myMachine = Machine("test_id")

dataStream = DataStream(myMachine)

dataStream.startJob("test_job_01")
dataStream.startProcessing("test_job_01")

sleep_time = 2

counter = 0

print("WHILE")
while counter <= 600:
    print("IT: ", counter)
    speedChange = random.uniform(0, 1)
    if (round(speedChange)):
        if (speedChange >= 0.75):
            myMachine.speed + 1
            sleep_time -= 0.1
        else:
            myMachine.speed - 1
            sleep_time += 0.1
    dataStream.input += 1
    outputBox = round(random.uniform(0.33, 1))
    if (outputBox):
        dataStream.output += 1    
    time.sleep(sleep_time)
    counter  += 1

dataStream.stopProcessing("test_job_01")
dataStream.endJob("test_job_01")

print("TERMINATE!")


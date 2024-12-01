from servo import Servo
from flask import Flask, request, jsonify
from gpiozero import DistanceSensor
from ir import IR
from ina import INA
from box_control import Box_control
from time import sleep

import threading

from DataStream import DataStream
from Machine import Machine

period = 0.05

app = Flask(__name__)

servo_pin = 17
ir_pin = 23

servo = Servo(servo_pin)
ir = IR(ir_pin)

distance_sensor = DistanceSensor(16, 20)
ina = INA()

id = "lauzhack-pi1"
myMachine = Machine(id)
myDataStream = DataStream(myMachine)

ir_state = False
distance_state = False

messages = []

@app.route('/set_velocity', methods=['POST'])
def set_velocity():
    data = request.get_json()
    if not data or 'velocity' not in data:
        return jsonify({'error': 'Missing "velocity" in request body'}), 400
    try:
        velocity = float(data['velocity'])
    except ValueError:
        return jsonify({'error': '"velocity" must be a float'}), 400
    try:
        servo.set_movement(velocity)
        myDataStream.changeSpeed(velocity)
        return jsonify({'message': 'Velocity set to {}'.format(velocity)})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    

@app.route('/start_job', methods=['POST'])
def start_job():
    myDataStream.startJob(id)
    return "OK"

@app.route('/end_job', methods=['POST'])
def end_job():
    myDataStream.endJob(id)
    return "OK"

@app.route('/start_processing', methods=['POST'])
def start_processing():
    myDataStream.sendTelemetry()
    myDataStream.startProcessing(id)
    return "OK"

@app.route('/stop_processing', methods=['POST'])
def stop_processing():
    myDataStream.stopProcessing(id)
    myDataStream.stopTelemetry()
    return "OK"

@app.route('/notifications')
def notifications():
    return jsonify(messages)

def communication(input, output, power):
    if input and not ir_state:
        myDataStream.newInputBox()
    if output and not distance_state:
        myDataStream.newOutputBox()
    myDataStream.increaseEnergy(power)

if __name__ == '__main__':
    t = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000)).start()
    bc = Box_control(ir)
    
    try:
        while True:
            distance = distance_sensor.distance
            output_detection =  1 if distance <= 0.1 else 0
            #print('Distance: {}'.format(distance))
            result = bc.check_box(servo.get_velocity())
            if result != None:
                messages.append(result)
            
            input_detection = ir.detect()
            #print('Object detected: {}'.format(input_detection))
            power = ina.read_power()
            #print('Power: {}'.format(power))

            communication(input_detection, output_detection, power)

            ir_state = input_detection
            distance_state = output_detection
            
            sleep(period)

    except KeyboardInterrupt:
        t.join()


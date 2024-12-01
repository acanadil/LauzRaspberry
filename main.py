from servo import Servo
from flask import Flask, request, jsonify
from gpiozero import DistanceSensor
from ir import IR
from ina import INA
from time import sleep
import threading

period = 1

app = Flask(__name__)

servo_pin = 17
ir_pin = 23

servo = Servo(servo_pin)
ir = IR(ir_pin)

distance_sensor = DistanceSensor(16, 20)
ina = INA()


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
        return jsonify({'message': 'Velocity set to {}'.format(velocity)})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    t = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000)).start()

    try:
        while True:
            distance = distance_sensor.distance
            print('Distance: {}'.format(distance))
            object_detected = ir.detect()
            print('Object detected: {}'.format(object_detected))
            power = ina.read_power()
            print('Power: {}'.format(power))
            sleep(period)

    except KeyboardInterrupt:
        t.join()


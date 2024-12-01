import RPi.GPIO as GPIO
import time

# declare the sensor and led pin
sensor_pin = 23

class IR:
    def __init__(self, sensor_pin):
        self.sensor_pin = sensor_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(sensor_pin, GPIO.IN)

    def detect(self):
        if GPIO.input(self.sensor_pin):
            return False
        else:
            return True
    
    def cleanup(self):
        #GPIO.cleanup()
        pass

# ir = IR(sensor_pin)

# try:
#     while True:
#         if ir.detect():
#             print("Obstacle detected")
#         else:
#             print("No obstacle detected")
#         time.sleep(1)
# except KeyboardInterrupt:
#     ir.cleanup()
#     print("Exiting program")

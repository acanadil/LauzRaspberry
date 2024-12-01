import RPi.GPIO as GPIO
from enum import Enum
import time


RIGHT = 2.5
LEFT = 12.5
STOP = 7.5

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    STOP = 3

class Servo:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        self.p = GPIO.PWM(pin, 50) # GPIO 17 for PWM with 50Hz
        self.p.start(STOP) # Initialization

    def set_movement(self, velocity):
        """
        Sets the servo movement
        :param velocity: The velocity to set the servo to, from -1 to 1, where -1 is full left, 0 is stop, and 1 is full right
        """
        if velocity < -1 or velocity > 1:
            raise ValueError("Velocity must be between -1 and 1")
        else:
            self.p.ChangeDutyCycle(velocity * 5 + 7.5)

    def cleanup(self):
        self.p.ChangeDutyCycle(STOP)
        self.p.stop()
        #GPIO.cleanup()

# s = Servo(servoPIN)

# try:
#     while True:
#         s.set_movement(1)
#         time.sleep(1)
#         s.set_movement(0)
#         time.sleep(1)
#         s.set_movement(-1)
#         time.sleep(1)
#         s.set_movement(0)
#         time.sleep(1)
# except KeyboardInterrupt:
#     s.cleanup()

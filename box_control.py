from ir import IR
import time

class Box_control:
    def __init__(self, ir):
        self.ir = ir
        self.prev_state = False
        self.timestamp = time.time()
        self.box_inf_thrshld = 1.5
        self.box_upp_thrshld = 1.8
        self.gap_inf_thrshld = 2.6
        self.gap_upp_thrshld = 2.9



    def check_box(self, angular_vel, buffer):
        ir_state = self.ir.detect()
        message = None
        if ir_state != self.prev_state:
            duration = (time.time() - self.timestamp) * abs(angular_vel)
            if ir_state == True:
                if duration < self.gap_inf_thrshld:
                    message = "TO MANY BOXES"
                elif duration > self.gap_upp_thrshld:
                    message = "MISSING BOXES"
                #print("Gap is: " + str(time.time() - self.timestamp))
            else:
                if duration > self.box_upp_thrshld:
                    message = "TO MANY BOXES"
                #print("Box is: " + str(time.time() - self.timestamp))
            self.timestamp = time.time()
            self.prev_state = ir_state
        return message
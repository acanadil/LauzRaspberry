from ina219 import INA219
from ina219 import DeviceRangeError

SHUNT_OHMS = 0.1


class INA:
    def __init__(self):
        self.ina = INA219(SHUNT_OHMS, busnum=1)
        self.ina.configure()

    def read_power(self):
        return self.ina.power()

# def read():
#     ina = INA219(SHUNT_OHMS, busnum=1)
#     ina.configure()

#     print("Bus Voltage: %.3f V" % ina.voltage())
#     try:
#         print("Bus Current: %.3f mA" % ina.current())
#         print("Power: %.3f mW" % ina.power())
#         print("Shunt voltage: %.3f mV" % ina.shunt_voltage())
#     except DeviceRangeError as e:
#         # Current out of device range with specified shunt resistor
#         print(e)

# read()

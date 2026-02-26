from machine import Pin, ADC
import utime

sensor = ADC(26)  # exemple : pin ADC

while True:
    value = sensor.read_u16()
    print(value)
    utime.sleep(0.5)

# import time
# import machine
# 
# sensor = machine.ADC(machine.Pin(26))
# 
# while True:
#     value = sensor.read_u16()
#     print(value)
#     time.sleep(0.5)
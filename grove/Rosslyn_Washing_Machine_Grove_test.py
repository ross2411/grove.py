import time, sys, math
from grove.grove_water_sensor import GroveWaterSensor

def Average(lst):
    return sum(lst) /len(lst)

PIN = 2
sensor = GroveWaterSensor(PIN)
queue = []
print('Detecting ...')
while True:
    value = sensor.value
    if sensor.value < 500:
        print("{}, Detected Water.".format(value))
    else:
        print("{}, Dry.".format(value))
    queue.append(value)
    if (len(queue) > 5):
        queue.pop(0)

    avg = Average(queue)
    if (avg < 500):
        print(f"Major water leak detected!!!!")
        exit(0)
    time.sleep(.1)
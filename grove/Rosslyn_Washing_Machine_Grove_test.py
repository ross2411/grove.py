import time
from grove.grove_water_sensor import GroveWaterSensor
import requests




def Average(lst):
    return sum(lst) /len(lst)

PIN = 2
sensor = GroveWaterSensor(PIN)
queue = []
print('Detecting ...')
while True:
    value = sensor.value
    if value < 500:
        print("{}, Detected Water.".format(value))
    else:
        print("{}, Dry.".format(value))
    queue.append(value)
    if (len(queue) > 10):
        queue.pop(0)

    avg = Average(queue)
    if (avg < 500):
        print(f"Major water leak detected!!!!")
        requests.post("https://ntfy.sh/rosslynwashingleak",
        data=f"Water leak detect behind the washing machine.  Average reading {avg}".encode(encoding='utf-8'))
        exit(0)
    time.sleep(.1)
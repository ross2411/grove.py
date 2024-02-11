import time
from datetime import datetime, timedelta
from grove.grove_water_sensor import GroveWaterSensor
import requests
import rosslyn_config as config

notify = config.notify
lastNotified = None

def Average(lst):
    return sum(lst) /len(lst)

def ShouldNotify(notifyFlag, lastNotified):
    if (lastNotified is None):
        return notifyFlag
    
    nextTimeToNotify = lastNotified + timedelta(minutes=30)
    return notifyFlag & (datetime.now() > nextTimeToNotify)

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
        if (ShouldNotify(notify, lastNotified)):
            print(f"Sending notification")
            # requests.post("https://ntfy.sh/rosslynwashingleak",
            #     data=f"Water leak detect behind the washing machine.  Average reading {avg}".encode(encoding='utf-8'))
            lastNotified = datetime.now()
        else:
            print(f"NOT sending notification")
    time.sleep(.1)
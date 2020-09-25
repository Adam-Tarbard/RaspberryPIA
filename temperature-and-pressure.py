#!/usr/bin/env python

import boto3
import time
from datetime import datetime 
from bmp280 import BMP280
from ltr559 import LTR559
from matrix11x7 import Matrix11x7
from matrix11x7.fonts import font3x5

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

print("""temperature-and-pressure.py - Displays the temperature and pressure.

Press Ctrl+C to exit!

""")

# Initialise Boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SensorData')


# Initialise the BMP280
bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus)
ltr559 = LTR559()
matrix11x7 = Matrix11x7()
matrix11x7.set_brightness(0.3)

while True:
    ltr559.update_sensor()
    lux = ltr559.get_lux()
    prox = ltr559.get_proximity() 
    temperature = bmp280.get_temperature()
    pressure = bmp280.get_pressure()
    print('{:05.2f}*C {:05.2f}hPa'.format(temperature, pressure))
    print("Lux: {:06.2f}, Proximity: {:04d}".format(lux, prox))
    now = datetime.utcnow()
    matrix11x7.clear()
    matrix11x7.write_string(("{:2.0f}".format(temperature)), y=1, font=font3x5)
    matrix11x7.show()
    
    PrimaryKey = 'Reading:RaspberryPiA'
    SortKey = now.strftime("%Y-%m-%d %H:%M:%S")

    response = table.put_item(
        Item={
            'SensorID': PrimaryKey,
            'Timestamp': SortKey,
            'Temperature Value': str(temperature),
            'Pressure Value': str(pressure),
            'Lux Value': str(lux),
            'Proximity Value': str(prox) 
        }
    )
    time.sleep(60)

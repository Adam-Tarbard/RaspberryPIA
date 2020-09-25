#!/usr/bin/env python

import json
import boto3
import time
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key

def query_sensor_data(event, context):
 dynamodb = boto3.resource('dynamodb')
 now = datetime.now()
 earlier = datetime.now() - timedelta(hours=24)
 table = dynamodb.Table('SensorData')
 response = table.query(
   KeyConditionExpression=Key("SensorID").eq("Reading:RaspberryPiA") & Key('Timestamp').between(earlier.strftime("%Y-%m-%d %H:%M:%S"), now.strftime("%Y-%m-%d %H:%M:%S"))
        
 )
 return response

dataitems = query_sensor_data('','')['Items']
print(json.dumps(dataitems,indent=2))

now = datetime.now()

temperaturetest = 'Temperature Value'
temptot = 0
tempcount = 0

pressuretest = 'Pressure Value'
pressuretot = 0
pressurecount = 0

luxtest = 'Lux Value'
luxtot = 0
luxcount = 0

for item in dataitems:
  if temperaturetest in item:
    temptot = temptot + float(item['Temperature Value']) 
    tempcount = tempcount + 1

  if pressuretest in item:
    pressuretot = pressuretot + float(item['Pressure Value'])
    pressurecount = pressurecount + 1

  if luxtest in item:
    luxtot = luxtot + float(item['Lux Value'])
    luxcount = luxcount + 1
  
tempave = temptot / tempcount

pressureave = pressuretot / pressurecount

luxave = luxtot / luxcount

SortKey = now.strftime("%Y-%m-%d %H")
SecondaryKey = 'MeanRecord:RaspberryPiA'

recorddict = {
        "SensorID": SecondaryKey,
        "Timestamp": SortKey,
        "Temperature Average Value": str(tempave),
        "Presure Average Value": str(pressureave),
        "Lux Average Value": str(luxave)
        }


print('Average Values  Temperature: {}  Pressure: {}  Lux: {}'.format(tempave, pressureave, luxave)) 

#!/usr/bin/env python

import json
import boto3
import time
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SensorData')

def query_sensor_data(event, context):
  now = datetime.utcnow()
  earlier = datetime.utcnow() - timedelta(hours=24)
  response = table.query(
    KeyConditionExpression=Key("SensorID").eq("Reading:RaspberryPiA") & Key('Timestamp').between(earlier.strftime("%Y-%m-%d %H:%M:%S"), now.strftime("%Y-%m-%d %H:%M:%S"))
        
  )
  create_summary(response)
  return



def create_summary(ddbresponse):
  dataitems = ddbresponse['Items']
  
  # Initialize variables for averages
  temperaturetest = 'Temperature Value'
  temptot = 0
  tempcount = 0

  pressuretest = 'Pressure Value'
  pressuretot = 0
  pressurecount = 0

  luxtest = 'Lux Value'
  luxtot = 0
  luxcount = 0

  # For loop to sum totals and counts
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

  # Calculating Means  
  tempave = temptot / tempcount
  pressureave = pressuretot / pressurecount
  luxave = luxtot / luxcount

  # Set record keys
  now = datetime.now()
  SortKey = now.strftime("%Y-%m-%d %H:00:00")
  PrimaryKey = 'MeanRecord:RaspberryPiA'

  # Creating dictionary
  recorddict = {
          "SensorID": PrimaryKey,
          "Timestamp": SortKey,
          "Temperature Average Value": str(tempave),
          "Presure Average Value": str(pressureave),
          "Lux Average Value": str(luxave)
          }

  response = table.put_item(
      Item= recorddict)

  print('Average Values  Temperature: {}  Pressure: {}  Lux: {}'.format(tempave, pressureave, luxave)) 
 
  return

# For testing
# query_sensor_data('','')

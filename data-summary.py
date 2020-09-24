#!/usr/bin/env python

import json
import boto3
import time
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key

def query_sensor_data(event, context):
 dynamodb = boto3.resource('dynamodb')
 now = datetime.now()
 earlier = datetime.now() - timedelta(hours=5)
 table = dynamodb.Table('SensorData')
 response = table.query(
   KeyConditionExpression=Key("SensorID").eq("Reading:RaspberryPiA") & Key('Timestamp').between(earlier.strftime("%Y-%m-%d %H:%M:%S"), now.strftime("%Y-%m-%d %H:%M:%S"))
        
 )
 return response

print(json.dumps(query_sensor_data('','')['Items'],indent=2))


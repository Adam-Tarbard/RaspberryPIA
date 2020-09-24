#!/usr/bin/env python

import json
import boto3
from boto3.dynamodb.conditions import Key

def query_sensor_data(event, context):
 dynamodb = boto3.resource('dynamodb')
 
 table = dynamodb.Table('SensorData')
 response = table.query(
   KeyConditionExpression=Key("SensorID").eq("Reading:RaspberryPiA") & Key('Timestamp').gt('2020-09-24')    
        
 )
 return response

print(json.dumps(query_sensor_data('','')['Items'],indent=2))


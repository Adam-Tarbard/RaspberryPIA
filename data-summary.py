#!/usr/bin/env python

import boto3
import json
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SensorData')

client = boto3.resource('dynamodb')
table = client.Table('SensorData')

def lambda_handler(event, context):

      response = table.query(
        KeyConditionExpression=Key('SensorID').eq('Reading:RaspberryPiA') & Key('Timestamp').gt('2020-09-20')    
        
      )
    
      items = response['items']
      for item in items:
         print('items')



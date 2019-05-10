from update import bar

import unittest
import datetime
import time
import json
import os
import boto3
from moto import mock_dynamodb2

##
# Test the Update methods
##
class TestUpdate(unittest.TestCase):

    ##
    # Tests update bar option with no Event
    ##
    def test_update_bar_empty(self):
        try:
            bar(None, None)
        except Exception as e:
            self.assertEquals("Couldn't update the bar, no body supplied.", e.message)

    ##
    # Tests update bar option with no id
    ##
    def test_update_bar_no_id(self):
        event = {}
        event['body'] = '{"name": "Test"}'

        try:
            bar(event, None)
        except Exception as e:
            self.assertEquals("Couldn't update the bar, no bar id supplied.", e.message)

    ##
    # Tests update bar option no matching item
    ##
    @mock_dynamodb2
    def test_update_bar_no_item(self):

        # Mock out DynamoDB
        dynamo = boto3.client('dynamodb', region_name='us-east-1')
        dynamo.create_table(
            TableName='swayze-life-bar-dev',
            KeySchema=[{
                'AttributeName': 'id',
                'KeyType': 'HASH'
            }],
            AttributeDefinitions=[{
                'AttributeName': 'id',
                'AttributeType': 'S'
            }],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            })

        # Mock out the Test Event and Path ID
        event = {}
        event['body'] = '{"name": "Test", "address": "2 Boston 2"}'
        event['pathParameters'] = {}
        event['pathParameters']['id'] = '999'

        # Set the table environment name
        os.environ['DYNAMODB_BAR_TABLE'] = 'swayze-life-bar-dev'

        # Test
        res = bar(event, None)
        self.assertEquals(400, res['statusCode'])

    ##
    # Test a successful bar option update
    ##
    @mock_dynamodb2
    def test_update_bar(self):

        # Mock out DynamoDB
        dynamo = boto3.client('dynamodb', region_name='us-east-1')
        dynamo.create_table(
            TableName='swayze-life-bar-dev',
            KeySchema=[{
                'AttributeName': 'id',
                'KeyType': 'HASH'
            }],
            AttributeDefinitions=[{
                'AttributeName': 'id',
                'AttributeType': 'S'
            }],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            })

        # Setup Test Data - this needs to be in DynamoDB JSON format
        initialData = {}
        initialData['id'] = { 'S': '123' }
        initialData['name'] = { 'S': 'old' }
        initialData['address'] = { 'S': '1 Boston St' }
        initialData['lat'] = { 'S': '1' }
        initialData['long'] = { 'S': '-1' }

        dynamo.put_item(
            TableName='swayze-life-bar-dev',
            Item=initialData)

        # Mock out the Test Event and Path ID
        event = {}
        event['body'] = '{"name": "new"}'
        event['pathParameters'] = {}
        event['pathParameters']['id'] = '123'

        # Set the table environment name
        os.environ['DYNAMODB_BAR_TABLE'] = 'swayze-life-bar-dev'

        # Test
        res = bar(event, None)
        self.assertEquals(200, res['statusCode'])

if __name__ == '__main__':
    unittest.main()

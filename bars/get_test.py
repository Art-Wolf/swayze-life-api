from get import bar

import unittest
import datetime
import time
import json
import os
import boto3
from moto import mock_dynamodb2

##
# Test the Get methods
##
class TestGet(unittest.TestCase):

    ##
    # Tests get bar option with no id
    ##
    def test_get_bar_no_id(self):
        event = {}

        try:
            bar(event, None)
        except Exception as e:
            self.assertEquals("No bar id supplied in event.", e.message)

    ##
    # Tests get bar option no matching item
    ##
    @mock_dynamodb2
    def test_get_bar_no_item(self):

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
        event['pathParameters'] = {}
        event['pathParameters']['id'] = '123'

        # Set the table environment name
        os.environ['DYNAMODB_BAR_TABLE'] = 'swayze-life-bar-dev'

        # Test
        res = bar(event, None)
        self.assertEquals(400, res['statusCode'])

    ##
    # Test a successful bar option get
    ##
    @mock_dynamodb2
    def test_get_bar(self):

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
        event['pathParameters'] = {}
        event['pathParameters']['id'] = '123'

        # Set the table environment name
        os.environ['DYNAMODB_BAR_TABLE'] = 'swayze-life-bar-dev'

        # Test
        res = bar(event, None)
        self.assertEquals(200, res['statusCode'])

if __name__ == '__main__':
    unittest.main()

from update import bingo

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
    # Tests update bingo option with no Event
    ##
    def test_update_bingo_empty(self):
        try:
            bingo(None, None)
        except Exception as e:
            self.assertEquals("Couldn't update the bingo option, no body supplied.", e.message)

    ##
    # Tests update bingo option with no id
    ##
    def test_update_bingo_no_id(self):
        event = {}
        event['body'] = '{"image": "Test"}'

        try:
            bingo(event, None)
        except Exception as e:
            self.assertEquals("Couldn't update the bingo option, no bingo id supplied.", e.message)

    ##
    # Tests update bingo option no matching item
    ##
    @mock_dynamodb2
    def test_update_bingo_no_item(self):

        # Mock out DynamoDB
        dynamo = boto3.client('dynamodb', region_name='us-east-1')
        dynamo.create_table(
            TableName='swayze-life-bingo-dev',
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
        event['body'] = '{"name": "Test", "image": "http://google.com"}'
        event['pathParameters'] = {}
        event['pathParameters']['id'] = '999'

        # Set the table environment name
        os.environ['DYNAMODB_BINGO_TABLE'] = 'swayze-life-bingo-dev'

        # Test
        res = bingo(event, None)
        self.assertEquals(400, res['statusCode'])

    ##
    # Test a successful bingo option update
    ##
    @mock_dynamodb2
    def test_update_bingo(self):

        # Mock out DynamoDB
        dynamo = boto3.client('dynamodb', region_name='us-east-1')
        dynamo.create_table(
            TableName='swayze-life-bingo-dev',
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

        dynamo.put_item(
            TableName='swayze-life-bingo-dev',
            Item=initialData)

        # Mock out the Test Event and Path ID
        event = {}
        event['body'] = '{"name": "new", "image": "http://google2.com"}'
        event['pathParameters'] = {}
        event['pathParameters']['id'] = '123'

        # Set the table environment name
        os.environ['DYNAMODB_BINGO_TABLE'] = 'swayze-life-bingo-dev'

        # Test
        res = bingo(event, None)
        self.assertEquals(200, res['statusCode'])

if __name__ == '__main__':
    unittest.main()

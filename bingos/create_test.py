from create import bingo

import unittest
import datetime
import time
import json
import os
import boto3
from moto import mock_dynamodb2

dynamodb = boto3.resource('dynamodb')

##
# Test the Create methods
##
class TestCreate(unittest.TestCase):

    ##
    # Tests create bingo option with no Event
    ##
    def test_create_bingo_empty(self):
        try:
            bingo(None, None)
        except Exception as e:
            self.assertEquals("Couldn't create the bingo option, no body supplied.", e.message)

    ##
    # Tests create bingo option with only the name set
    ##
    def test_create_bingo_name_only(self):
        event = {}
        event['body'] = '{"name": "Test"}'

        try:
            bingo(event, None)
        except Exception as e:
            self.assertEquals("Couldn't create the bingo option, no image.", e.message)

    ##
    # Tests create bingo option with only the image set
    ##
    def test_create_bingo_address_only(self):
        event = {}
        event['body'] = '{"image": "whatever"}'

        try:
            bingo(event, None)
        except Exception as e:
            self.assertEquals("Couldn't create the bingo option, no name.", e.message)

    ##
    # Tests a successful create bingo option
    ##
    @mock_dynamodb2
    def test_create_bingo(self):

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

        # Mock out the Test Event
        event = {}
        event['body'] = '{"name": "Test", "image": "whatever"}'

        # Set the table environment name
        os.environ['DYNAMODB_BINGO_TABLE'] = 'swayze-life-bingo-dev'

        # Test
        res = bingo(event, None)
        self.assertEquals(200, res['statusCode'])

if __name__ == '__main__':
    unittest.main()

from create import bar

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
    # Tests create bar option with no Event
    ##
    def test_create_bar_empty(self):
        try:
            bar(None, None)
        except Exception as e:
            self.assertEquals("Couldn't create the bar, no body supplied.", e.message)

    ##
    # Tests create bar option with only the name set
    ##
    def test_create_bar_name_only(self):
        event = {}
        event['body'] = '{"name": "Test"}'

        try:
            bar(event, None)
        except Exception as e:
            self.assertEquals("Couldn't create the bar, no auth0.", e.message)

    ##
    # Tests a successful create bar option
    ##
    @mock_dynamodb2
    def test_create_bar(self):

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

        # Mock out the Test Event
        event = {}
        event['body'] = '{"name": "Test", "auth0": "whatever"}'

        # Set the table environment name
        os.environ['DYNAMODB_BAR_TABLE'] = 'swayze-life-bar-dev'

        # Test
        res = bar(event, None)
        self.assertEquals(200, res['statusCode'])

if __name__ == '__main__':
    unittest.main()

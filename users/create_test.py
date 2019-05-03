from create import user

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
    # Tests create user option with no Event
    ##
    def test_create_user_empty(self):
        try:
            user(None, None)
        except Exception as e:
            self.assertEquals("Couldn't create the user, no body supplied.", e.message)

    ##
    # Tests create user option with only the name set
    ##
    def test_create_user_name_only(self):
        event = {}
        event['body'] = '{"name": "Test"}'

        try:
            user(event, None)
        except Exception as e:
            self.assertEquals("Couldn't create the user, no auth0.", e.message)

    ##
    # Tests create user option with only the auth0 set
    ##
    def test_create_user_auth0_only(self):
        event = {}
        event['body'] = '{"auth0": "whatever"}'

        try:
            user(event, None)
        except Exception as e:
            self.assertEquals("Couldn't create the user, no name.", e.message)

    ##
    # Tests a successful create user option
    ##
    @mock_dynamodb2
    def test_create_user(self):

        # Mock out DynamoDB
        dynamo = boto3.client('dynamodb', region_name='us-east-1')
        dynamo.create_table(
            TableName='swayze-life-user-dev',
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
        os.environ['DYNAMODB_USER_TABLE'] = 'swayze-life-user-dev'

        # Test
        res = user(event, None)
        self.assertEquals(200, res['statusCode'])

if __name__ == '__main__':
    unittest.main()

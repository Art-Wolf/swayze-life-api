from complete import bingo

import unittest
import datetime
import time
import json
import os
import boto3
from moto import mock_dynamodb2

##
# Test the Complete methods
##
class TestGet(unittest.TestCase):

    ##
    # Tests complete bingo option with no id
    ##
    def test_complere_bingo_no_id(self):
        event = {}

        try:
            bingo(event, None)
        except Exception as e:
            self.assertEquals("Couldn't complete the bingo option, no bingo id supplied.", e.message)

    ##
    # Test a successful bingo option get
    ##
    @mock_dynamodb2
    def test_complete_bingo(self):

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

        # Setup Test Data - this needs to be in DynamoDB JSON format
        initialBingoData = {}
        initialBingoData['id'] = { 'S': '123' }
        initialBingoData['completed'] = { 'BOOL': False }

        dynamo.put_item(
            TableName='swayze-life-bingo-dev',
            Item=initialBingoData)

        initialUserData = {}
        initialUserData['id'] = { 'S': '123' }
        initialUserData['bingoList'] = {'L':[{'M': {'id': { 'S': '123' }, 'completed': { 'BOOL': False}}},{'M': {'id': { 'S': '456' }, 'completed': { 'BOOL': False}}},{'M': {'id': { 'S': '456' }, 'completed': { 'BOOL': False}}},{'M': {'id': { 'S': '456' }, 'completed': { 'BOOL': False}}},{'M': {'id': { 'S': '456' }, 'completed': { 'BOOL': False}}},{'M': {'id': { 'S': '456' }, 'completed': { 'BOOL': False}}},{'M': {'id': { 'S': '456' }, 'completed': { 'BOOL': False}}},{'M': {'id': { 'S': '456' }, 'completed': { 'BOOL': False}}},{'M': {'id': { 'S': '456' }, 'completed': { 'BOOL': False}}},{'M': {'id': { 'S': '456' }, 'completed': { 'BOOL': False}}},{'M': {'id': { 'S': '456' }, 'completed': { 'BOOL': False}}},{'M': {'id': { 'S': '456' }, 'completed': { 'BOOL': False}}},{'M': {'id': { 'S': '456' }, 'completed': { 'BOOL': False}}},{'M': {'id': { 'S': '456' }, 'completed': { 'BOOL': False}}},{'M': {'id': { 'S': '456' }, 'completed': { 'BOOL': False}}},{'M': {'id': { 'S': '456' }, 'completed': { 'BOOL': False}}}]}

        dynamo.put_item(
            TableName='swayze-life-user-dev',
            Item=initialUserData)

        # Mock out the Test Event and Path ID
        event = {}
        event['pathParameters'] = {}
        event['pathParameters']['id'] = '123'

        # Set the table environment name
        os.environ['DYNAMODB_BINGO_TABLE'] = 'swayze-life-bingo-dev'
        os.environ['DYNAMODB_USER_TABLE'] = 'swayze-life-user-dev'

        # Test
        res = bingo(event, None)
        self.assertEquals(200, res['statusCode'])

if __name__ == '__main__':
    unittest.main()

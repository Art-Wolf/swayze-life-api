from list import bar

import unittest
import json
import os
import boto3
from moto import mock_dynamodb2

##
# Test the List methods
##
class TestList(unittest.TestCase):

    ##
    # Test a successful bar list
    ##
    @mock_dynamodb2
    def test_list_bar(self):

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

        # Set the table environment name
        os.environ['DYNAMODB_BAR_TABLE'] = 'swayze-life-bar-dev'

        # Test
        res = bar(None, None)
        self.assertEquals(200, res['statusCode'])
        item_dict = json.loads(res['body'])
        self.assertEquals(1, len(item_dict))

if __name__ == '__main__':
    unittest.main()

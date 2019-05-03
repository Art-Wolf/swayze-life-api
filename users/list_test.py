from list import user

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
    # Test a successful user list
    ##
    @mock_dynamodb2
    def test_list_user(self):

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

        # Setup Test Data - this needs to be in DynamoDB JSON format
        initialData = {}
        initialData['id'] = { 'S': '123' }
        initialData['name'] = { 'S': 'old' }

        dynamo.put_item(
            TableName='swayze-life-user-dev',
            Item=initialData)

        # Set the table environment name
        os.environ['DYNAMODB_USER_TABLE'] = 'swayze-life-user-dev'

        # Test
        res = user(None, None)
        self.assertEquals(200, res['statusCode'])
        item_dict = json.loads(res['body'])
        self.assertEquals(1, len(item_dict))

if __name__ == '__main__':
    unittest.main()

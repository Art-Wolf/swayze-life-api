import json
import logging
import os
import time
import uuid
import random
import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr

##
# Helper class to convert a DynamoDB item to JSON.
##
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

##
# Configure the logger
##
root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)
logging.basicConfig(format='%(asctime)s %(message)s',level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

##
# Update the bar option in the dynamodb Table
##
def bar(event, context):
    logger.info("Entering update bar")
    logger.info("Received Event: {}".format(event))

    # Make sure we got data to update with
    if (event is None) or ('body' not in event):
        logger.error("Couldn't update the bar, no body supplied.")
        raise Exception("Couldn't update the bar, no body supplied.")

    # Make sure we got an ID from the path
    if ('pathParameters' not in event) or ('id' not in event['pathParameters']):
        logger.error("Couldn't update the bar, no bar id supplied.")
        raise Exception("Couldn't update the bar, no bar id supplied.")

    data = json.loads(event['body'])

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_BAR_TABLE'])

    confirm = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    # If there was no data to get, we get back an empty string
    if not confirm.get("Item"):
        logger.error("No bar to Get")
        response = {
            "statusCode": 400,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": "No bar option to Get"
        }
    else:
        timestamp = int(time.time() * 1000)
        result = table.update_item(
            Key={
                'id': event['pathParameters']['id']
            },
            ExpressionAttributeValues={
              'name': data['name'],
              'address': data['address'],
              'lat': data['lat'],
              'long': data['long'],
              'order': data['order'],
              'complete': data['complete'],
              ':updatedAt': timestamp,
            },
            UpdateExpression='SET name = :name, address = :address, lat = :lat, long = :long, order = :order, complete = :complete, updatedAt = :updatedAt ',
            ReturnValues='ALL_NEW',
        )

        # If there was no data to update, we get back an empty string
        if not result['Attributes']:
            logger.error("No bar to Update")
            response = {
                "statusCode": 400,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": "No bar to Update"
            }
        else:
            response = {
                "statusCode": 200,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps(result['Attributes'], cls=DecimalEncoder)
            }

    logger.info("Returning Response: {}".format(response));

    return response

import json
import logging
import os
import time
import uuid
import random
import boto3
import random
import decimal

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
# Required variables
##
keys = ['name']

##
# Validate that the required variables were set
##
def validateReq(data, keys):
    for item in keys:
        if item not in data:
            logger.error("Couldn't create the bar, no %s." % item)
            raise Exception("Couldn't create the bar, no %s." % item)

##
# Create the bar option
##
def bar(event, context):
    logger.info("Entering create bar")
    logger.info("Received Event: {}".format(event))

    # Make sure we got data to update with
    if (event is None) or (event['body'] is None):
        logger.error("Couldn't create the bar, no body supplied.")
        raise Exception("Couldn't create the bar, no body supplied.")

    data = json.loads(event['body'])
    validateReq(data, keys)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_BAR_TABLE'])

    timestamp = int(time.time() * 1000)
    item = {
        'id': str(uuid.uuid1()),
        'name': data['name'],
        'address': data['address'],
        'lat': data['lat'],
        'long': data['long'],
        'order': data['order'],
        'complete': False,
        'createdAt': timestamp,
        'updatedAt': timestamp,
    }

    logger.info("Creating bar: {}".format(item));

    # write the data to the database
    newItem = table.put_item(Item=item)

    # create a response
    response = {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps(item, cls=DecimalEncoder)
    }

    logger.info("Returning Response: {}".format(response));
    return response

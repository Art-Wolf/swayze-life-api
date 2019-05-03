import json
import logging
import os
import time
import uuid
import random
import boto3


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
keys = ['name', 'blurb', 'icon', 'image']

##
# Validate that the required variables were set
##
def validateReq(data, keys):
    for item in keys:
        if item not in data:
            logger.error("Couldn't create the bingo option, no %s." % item)
            raise Exception("Couldn't create the bingo option, no %s." % item)

##
# Create the bingo option
##
def bingo(event, context):
    logger.info("Entering create bingo option")
    logger.info("Received Event: {}".format(event))

    # Make sure we got data to update with
    if (event is None) or (event['body'] is None):
        logger.error("Couldn't create the bingo option, no body supplied.")
        raise Exception("Couldn't create the bingo option, no body supplied.")

    data = json.loads(event['body'])
    validateReq(data, keys)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_BINGO_TABLE'])

    timestamp = int(time.time() * 1000)
    item = {
        'id': str(uuid.uuid1()),
        'name': data['name'],
        'blurb': data['blurb'],
        'icon': data['icon'],
        'image': data['image'],
        'completed': False,
        'createdAt': timestamp,
        'updatedAt': timestamp,
    }

    logger.info("Creating Bingo option: {}".format(item));

    # write the data to the database
    newItem = table.put_item(Item=item)

    # create a response
    response = {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps(item)
    }

    logger.info("Returning Response: {}".format(response));
    return response

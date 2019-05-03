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
keys = ['name', 'auth0']

##
# Validate that the required variables were set
##
def validateReq(data, keys):
    for item in keys:
        if item not in data:
            logger.error("Couldn't create the user, no %s." % item)
            raise Exception("Couldn't create the user, no %s." % item)

##
# Create the user option
##
def user(event, context):
    logger.info("Entering create user")
    logger.info("Received Event: {}".format(event))

    # Make sure we got data to update with
    if (event is None) or (event['body'] is None):
        logger.error("Couldn't create the user, no body supplied.")
        raise Exception("Couldn't create the user, no body supplied.")

    data = json.loads(event['body'])
    validateReq(data, keys)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_USER_TABLE'])

    timestamp = int(time.time() * 1000)
    item = {
        'id': str(uuid.uuid1()),
        'name': data['name'],
        'auth0': data['auth0'],
        'createdAt': timestamp,
        'updatedAt': timestamp,
    }

    logger.info("Creating user: {}".format(item));

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

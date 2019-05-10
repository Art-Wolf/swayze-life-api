import json
import logging
import os
import decimal
import boto3

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
# Get the list of bar options from the dynamodb Table
##
def bar(event, context):
    logger.info("Entering list bar options")

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_BAR_TABLE'])

    # fetch all todos from the database
    result = table.scan()

    # create a response
    response = {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps(result['Items'], cls=DecimalEncoder)
    }

    return response

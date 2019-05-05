import json
import logging
import os
import time
import uuid
import random
import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
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

def calculateScore(user):
    logger.info("Entering calculateScore")
    column_1 = 4
    column_2 = 4
    column_3 = 4
    column_4 = 4
    row_1 = 4
    row_2 = 4
    row_3 = 4
    row_4 = 4

    if (user['bingoList'][0]['complete']):
        logger.info("Users index 0 is complete")
        column_1 -= 1
        row_1 -= 1
    if (user['bingoList'][1]['complete']):
        logger.info("Users index 1 is complete")
        column_1 -= 1
        row_2 -= 1
    if (user['bingoList'][2]['complete']):
        logger.info("Users index 2 is complete")
        column_1 -= 1
        row_3 -= 1
    if (user['bingoList'][3]['complete']):
        logger.info("Users index 3 is complete")
        column_1 -= 1
        row_4 -= 1
    if (user['bingoList'][4]['complete']):
        logger.info("Users index 4 is complete")
        column_2 -= 1
        row_1 -= 1
    if (user['bingoList'][5]['complete']):
        logger.info("Users index 5 is complete")
        column_2 -= 1
        row_2 -= 1
    if (user['bingoList'][6]['complete']):
        logger.info("Users index 6 is complete")
        column_2 -= 1
        row_3 -= 1
    if (user['bingoList'][7]['complete']):
        logger.info("Users index 7 is complete")
        column_2 -= 1
        row_4 -= 1
    if (user['bingoList'][8]['complete']):
        logger.info("Users index 8 is complete")
        column_3 -= 1
        row_1 -= 1
    if (user['bingoList'][9]['complete']):
        logger.info("Users index 9 is complete")
        column_3 -= 1
        row_2 -= 1
    if (user['bingoList'][10]['complete']):
        logger.info("Users index 10 is complete")
        column_3 -= 1
        row_3 -= 1
    if (user['bingoList'][11]['complete']):
        logger.info("Users index 11 is complete")
        column_3 -= 1
        row_4 -= 1
    if (user['bingoList'][12]['complete']):
        logger.info("Users index 12 is complete")
        column_4 -= 1
        row_1 -= 1
    if (user['bingoList'][13]['complete']):
        logger.info("Users index 13 is complete")
        column_4 -= 1
        row_2 -= 1
    if (user['bingoList'][14]['complete']):
        logger.info("Users index 14 is complete")
        column_4 -= 1
        row_3 -= 1
    if (user['bingoList'][15]['complete']):
        logger.info("Users index 15 is complete")
        column_4 -= 1
        row_4 -= 1

    if column_1 <= column_2 and column_1 <= column_3 and column_1 <= column_4 and column_1 <= row_1 and column_1 <= row_2 and column_1 <= row_3 and column_1 <= row_4:
        logger.info("Column 1 is the shortest with {} spaces to go.".format(column_1))
        return column_1
    if column_2 <= column_1 and column_2 <= column_3 and column_2 <= column_4 and column_2 <= row_1 and column_2 <= row_2 and column_2 <= row_3 and column_2 <= row_4:
        logger.info("Column 2 is the shortest with {} spaces to go.".format(column_2))
        return column_2
    if column_3 <= column_1 and column_3 <= column_2 and column_3 <= column_4 and column_3 <= row_1 and column_3 <= row_2 and column_3 <= row_3 and column_3 <= row_4:
        logger.info("Column 3 is the shortest with {} spaces to go.".format(column_3))
        return column_3
    if column_4 <= column_1 and column_4 <= column_2 and column_4 <= column_3 and column_4 <= row_1 and column_4 <= row_2 and column_4 <= row_3 and column_4 <= row_4:
        logger.info("Column 4 is the shortest with {} spaces to go.".format(column_4))
        return column_4
    if row_1 <= column_1 and row_1 <= column_2 and row_1 <= column_3 and row_1 <= column_4 and row_1 <= row_2 and row_1 <= row_3 and row_1 <= row_4:
        logger.info("Row 1 is the shortest with {} spaces to go.".format(row_1))
        return row_1
    if row_2 <= column_1 and row_2 <= column_2 and row_2 <= column_3 and row_2 <= column_4 and row_2 <= row_1 and row_2 <= row_3 and row_2 <= row_4:
        logger.info("Row 2 is the shortest with {} spaces to go.".format(row_2))
        return row_2
    if row_3 <= column_1 and row_3 <= column_2 and row_3 <= column_3 and row_3 <= column_4 and row_3 <= row_1 and row_3 <= row_2 and row_3 <= row_4:
        logger.info("Row 3 is the shortest with {} spaces to go.".format(row_3))
        return row_3
    if row_4 <= column_1 and row_4 <= column_2 and row_4 <= column_3 and row_4 <= column_4 and row_4 <= row_1 and row_4 <= row_2 and row_4 <= row_3:
        logger.info("Row 4 is the shortest with {} spaces to go.".format(row_4))
        return row_4

    return 5
##
# Update the bingo option in the dynamodb Table
##
def bingo(event, context):
    logger.info("Entering complete bingo option")
    logger.info("Received Event: {}".format(event))

    # Make sure we got an ID from the path
    if ('pathParameters' not in event) or ('id' not in event['pathParameters']):
        logger.error("Couldn't complete the bingo option, no bingo id supplied.")
        raise Exception("Couldn't complete the bingo option, no bingo id supplied.")

    dynamodb = boto3.resource('dynamodb')
    bingo_table = dynamodb.Table(os.environ['DYNAMODB_BINGO_TABLE'])
    user_table = table = dynamodb.Table(os.environ['DYNAMODB_USER_TABLE'])

    confirm = bingo_table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    # If there was no data to get, we get back an empty string
    if not confirm.get("Item"):
        logger.error("No Bingo option to Get")
        response = {
            "statusCode": 400,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": "No Bingo option to Get"
        }
    else:
        timestamp = int(time.time() * 1000)

        try:
            result = bingo_table.update_item(
                Key={
                    'id': confirm['Item']['id']
                },
                ExpressionAttributeValues={
                  ':completed': True,
                  ':updatedAt': timestamp,
                },
                UpdateExpression='SET completed = :completed, updatedAt = :updatedAt ',
                ReturnValues='ALL_NEW',
            )

            # If there was no data to update, we get back an empty string
            if not result['Attributes']:
                logger.error("No Bingo option to Update")
                response = {
                    "statusCode": 400,
                    "headers": {"Access-Control-Allow-Origin": "*"},
                    "body": "No Bingo option to Update"
                }
            else:
                # Need to update all the users now also.
                user_result = user_table.scan()

                for user in user_result['Items']:

                    for bingo in user['bingoList']:
                        if (bingo['id'] == event['pathParameters']['id']):
                            bingo['completed'] = True

                    user_result = user_table.update_item(
                        Key={
                            'id': user['id']
                        },
                        ExpressionAttributeValues={
                          ':bingoList': user['bingoList'],
                          ':squaresToGo': calculateScore(user),
                          ':updatedAt': timestamp,
                        },
                        UpdateExpression='SET bingoList = :bingoList, updatedAt = :updatedAt, squaresToGo = :squaresToGo ',
                        ReturnValues='ALL_NEW',
                    )

                response = {
                    "statusCode": 200,
                    "headers": {"Access-Control-Allow-Origin": "*"},
                    "body": json.dumps(result['Attributes'], cls=DecimalEncoder)
                }
        except ClientError as e:
            response = {
                "statusCode": 400,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": "No Bingo option to Update"
            }

    logger.info("Returning Response: {}".format(response));

    return response

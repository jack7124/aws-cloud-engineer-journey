import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("Properties")
# note: need decimal conversions for handling

def decimal_to_number(value):
    if isinstance(value, Decimal):
        return int(value) if value == value.to_integral_value() else float(value)
    raise TypeError(f"Cannot serialize {type(value).__name__}")


def lambda_handler(event, context):
    listing_id = event["pathParameters"]["id"]
    response = table.get_item(Key={"L_ListingID": listing_id})
    item = response.get("Item")

    return {
        "statusCode": 200 if item else 404,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(
            item if item else {"error": "not found"},
            default=decimal_to_number
        )
    }

"""GET /incidents — list incidents, optionally filtered by ?type= and/or ?status=.

Note: this uses a table Scan, which is fine at portfolio/demo scale (hundreds-
thousands of items). If you take this to production with a large table, add a
Global Secondary Index (e.g. on `status`) and Query instead of Scan.
"""
import json
import os
from decimal import Decimal

import boto3

if os.environ.get("AWS_SAM_LOCAL") == "true":
    dynamodb = boto3.resource(
        "dynamodb",
        endpoint_url="http://host.docker.internal:8000",
        region_name="us-east-1",
        aws_access_key_id="local",
        aws_secret_access_key="local",
    )
    table = dynamodb.Table("disaster-incidents-dev")
else:
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ["TABLE_NAME"])


def handler(event, context):
    params = event.get("queryStringParameters") or {}
    incident_type = params.get("type")
    status_filter = params.get("status")

    items = []
    scan_kwargs = {}
    while True:
        response = table.scan(**scan_kwargs)
        items.extend(response.get("Items", []))
        if "LastEvaluatedKey" not in response:
            break
        scan_kwargs["ExclusiveStartKey"] = response["LastEvaluatedKey"]

    if incident_type:
        items = [i for i in items if i.get("type") == incident_type]
    if status_filter:
        items = [i for i in items if i.get("status") == status_filter]

    items.sort(key=lambda i: i.get("createdAt", 0), reverse=True)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(items, default=lambda o: float(o) if isinstance(o, Decimal) else str(o)),
    }

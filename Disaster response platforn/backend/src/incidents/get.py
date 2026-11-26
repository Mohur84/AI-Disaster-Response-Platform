"""GET /incidents/{incidentId} — fetch a single incident."""
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
    incident_id = (event.get("pathParameters") or {}).get("incidentId")
    if not incident_id:
        return _response(400, {"error": "incidentId is required"})

    result = table.get_item(Key={"incidentId": incident_id})
    item = result.get("Item")

    if not item:
        return _response(404, {"error": "Incident not found"})

    return _response(200, item)


def _response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(body, default=lambda o: float(o) if isinstance(o, Decimal) else str(o)),
    }

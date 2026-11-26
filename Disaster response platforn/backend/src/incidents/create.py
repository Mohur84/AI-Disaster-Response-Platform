"""POST /incidents — create a new incident report.

Expected JSON body:
{
  "type": "flood" | "fire" | "earthquake" | "storm" | "other",
  "severity": "low" | "medium" | "high" | "critical",
  "lat": 34.0699,
  "lng": -118.4465,
  "description": "Optional free-text description"
}
"""
import json
import os
import time
import uuid
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

VALID_TYPES = {"flood", "fire", "earthquake", "storm", "other"}
VALID_SEVERITIES = {"low", "medium", "high", "critical"}


def handler(event, context):
    try:
        body = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return _response(400, {"error": "Invalid JSON body"})

    incident_type = body.get("type", "other")
    severity = body.get("severity", "low")
    lat = body.get("lat")
    lng = body.get("lng")
    description = (body.get("description") or "").strip()[:1000]

    if lat is None or lng is None:
        return _response(400, {"error": "lat and lng are required"})
    if incident_type not in VALID_TYPES:
        return _response(400, {"error": f"type must be one of {sorted(VALID_TYPES)}"})
    if severity not in VALID_SEVERITIES:
        return _response(400, {"error": f"severity must be one of {sorted(VALID_SEVERITIES)}"})

    try:
        lat = Decimal(str(lat))
        lng = Decimal(str(lng))
    except (ValueError, ArithmeticError):
        return _response(400, {"error": "lat and lng must be numbers"})

    incident_id = str(uuid.uuid4())
    now = int(time.time())

    item = {
        "incidentId": incident_id,
        "type": incident_type,
        "severity": severity,
        "lat": lat,
        "lng": lng,
        "description": description,
        "status": "reported",   # reported -> verified -> resolved
        "aiVerified": False,
        "aiLabels": [],
        "photoUrl": None,
        "createdAt": now,
        "updatedAt": now,
    }

    table.put_item(Item=item)

    return _response(201, item)


def _response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(body, default=_json_default),
    }


def _json_default(o):
    if isinstance(o, Decimal):
        return float(o)
    return str(o)

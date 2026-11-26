"""S3 ObjectCreated trigger (prefix: uploads/) — runs the photo through
Rekognition, and if the detected labels match the reported disaster type,
marks the incident as AI-verified. Verification changes the item's `status`,
which is what PublishAlertFunction (subscribed to the DynamoDB Stream) reacts
to for high/critical severity incidents.

S3 key format expected: uploads/{incidentId}/{filename}
"""
import json
import os
import re
import time
from urllib.parse import unquote_plus

import boto3

rekognition = boto3.client("rekognition")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

KEY_PATTERN = re.compile(r"^uploads/([^/]+)/")

# Rekognition labels that corroborate each reported incident type.
DISASTER_LABELS = {
    "flood": {"flood", "flooding", "water", "waterlogged"},
    "fire": {"fire", "flame", "smoke", "wildfire", "ash"},
    "storm": {"storm", "hurricane", "tornado", "lightning", "hail"},
    "earthquake": {"rubble", "debris", "collapsed", "wreckage"},
}


def handler(event, context):
    for record in event.get("Records", []):
        bucket = record["s3"]["bucket"]["name"]
        key = unquote_plus(record["s3"]["object"]["key"])

        match = KEY_PATTERN.match(key)
        if not match:
            continue
        incident_id = match.group(1)

        try:
            existing = table.get_item(Key={"incidentId": incident_id}).get("Item")
        except Exception:
            existing = None
        if not existing:
            # Photo uploaded for an incident that no longer exists — skip.
            continue

        rekognition_response = rekognition.detect_labels(
            Image={"S3Object": {"Bucket": bucket, "Name": key}},
            MaxLabels=15,
            MinConfidence=70,
        )

        labels = [
            {"name": label["Name"], "confidence": round(label["Confidence"], 1)}
            for label in rekognition_response.get("Labels", [])
        ]
        label_names = {label["name"].lower() for label in labels}

        reported_type = existing.get("type", "other")
        keywords = DISASTER_LABELS.get(reported_type, set())
        ai_verified = bool(label_names & keywords)

        update_expr = "SET aiLabels = :labels, aiVerified = :verified, photoUrl = :url, updatedAt = :now"
        expr_values = {
            ":labels": labels,
            ":verified": ai_verified,
            ":url": f"s3://{bucket}/{key}",
            ":now": int(time.time()),
        }
        expr_names = {}

        if ai_verified and existing.get("status") == "reported":
            update_expr += ", #s = :status"
            expr_values[":status"] = "verified"
            expr_names["#s"] = "status"

        table.update_item(
            Key={"incidentId": incident_id},
            UpdateExpression=update_expr,
            ExpressionAttributeValues=expr_values,
            **({"ExpressionAttributeNames": expr_names} if expr_names else {}),
        )

    return {"statusCode": 200, "body": json.dumps({"processed": len(event.get("Records", []))})}

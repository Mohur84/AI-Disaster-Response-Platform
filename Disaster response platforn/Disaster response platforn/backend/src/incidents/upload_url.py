"""POST /incidents/{incidentId}/upload-url

Returns a presigned S3 PUT URL so the browser can upload a photo directly to
S3 (never through API Gateway/Lambda — keeps large files off your Lambda
payload limits and off your compute bill). The upload lands under
`uploads/{incidentId}/...`, which is what tells AnalyzeImageFunction which
incident to attach its Rekognition results to.

Expected JSON body: { "filename": "photo.jpg", "contentType": "image/jpeg" }
"""
import json
import os
import re

import boto3

s3 = boto3.client("s3")
BUCKET = os.environ["PHOTOS_BUCKET"]

SAFE_FILENAME = re.compile(r"[^A-Za-z0-9_.-]")


def handler(event, context):
    incident_id = (event.get("pathParameters") or {}).get("incidentId")
    if not incident_id:
        return _response(400, {"error": "incidentId is required"})

    try:
        body = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return _response(400, {"error": "Invalid JSON body"})

    filename = SAFE_FILENAME.sub("_", body.get("filename", "photo.jpg"))
    content_type = body.get("contentType", "image/jpeg")

    if not content_type.startswith("image/"):
        return _response(400, {"error": "contentType must be an image/* type"})

    key = f"uploads/{incident_id}/{filename}"

    presigned_url = s3.generate_presigned_url(
        "put_object",
        Params={"Bucket": BUCKET, "Key": key, "ContentType": content_type},
        ExpiresIn=300,  # 5 minutes — plenty for a browser to start an upload
    )

    return _response(200, {"uploadUrl": presigned_url, "key": key})


def _response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(body),
    }

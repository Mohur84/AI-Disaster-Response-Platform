"""DynamoDB Streams trigger on the Incidents table — publishes an SNS alert
whenever a high/critical severity incident is created, or transitions status
(e.g. reported -> verified). Subscribe your email or phone number to the
AlertsTopic (see README) to receive these as email/SMS.
"""
import os

import boto3

sns = boto3.client("sns")
TOPIC_ARN = os.environ["ALERTS_TOPIC_ARN"]
ALERT_SEVERITIES = {"high", "critical"}


def handler(event, context):
    published = 0

    for record in event.get("Records", []):
        if record.get("eventName") not in ("INSERT", "MODIFY"):
            continue

        new_image = record.get("dynamodb", {}).get("NewImage", {})
        severity = new_image.get("severity", {}).get("S")
        if severity not in ALERT_SEVERITIES:
            continue

        status = new_image.get("status", {}).get("S")
        old_image = record.get("dynamodb", {}).get("OldImage", {})
        old_status = old_image.get("status", {}).get("S")

        # On MODIFY, only alert again if the status actually changed
        # (avoids re-alerting on every unrelated field update).
        if record["eventName"] == "MODIFY" and old_status == status:
            continue

        incident_type = new_image.get("type", {}).get("S", "unknown")
        incident_id = new_image.get("incidentId", {}).get("S", "unknown")
        description = new_image.get("description", {}).get("S", "")

        message_lines = [
            f"{severity.upper()} severity {incident_type} incident — status: {status}",
            f"Incident ID: {incident_id}",
        ]
        if description:
            message_lines.append(f"Description: {description}")

        sns.publish(
            TopicArn=TOPIC_ARN,
            Subject=f"Disaster alert: {incident_type} ({severity})"[:100],
            Message="\n".join(message_lines),
        )
        published += 1

    return {"statusCode": 200, "published": published}

import boto3

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://localhost:8000",
    region_name="us-east-1",
    aws_access_key_id="local",
    aws_secret_access_key="local",
)

table = dynamodb.create_table(
    TableName="disaster-incidents-dev",
    KeySchema=[
        {"AttributeName": "incidentId", "KeyType": "HASH"}
    ],
    AttributeDefinitions=[
        {"AttributeName": "incidentId", "AttributeType": "S"}
    ],
    BillingMode="PAY_PER_REQUEST",
)

print(f"Created table: {table.name}")
import boto3
import json


ecs_client = boto3.client('ecs')

def lambda_handler(event,context):
    print("Received event:",json.dumps(event))

    response = ecs_client.run_task(
        
    )
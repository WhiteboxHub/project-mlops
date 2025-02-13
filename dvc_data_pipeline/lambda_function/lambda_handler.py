import json
import boto3
import os

ecs_client = boto3.client("ecs")

def lambda_handler(event, context):
    print("Event received:", json.dumps(event))
    
    cluster_name = 'MLOpsCluster_aka'
    task_definition = "MLOpsTask_aka"

    response = ecs_client.run_task(
        cluster=cluster_name,
        launchType="FARGATE",
        taskDefinition=task_definition,
    )

    print("ECS Task triggered:", response)
    
    return {"statusCode": 200, "body": "ECS Task Started Successfully"}

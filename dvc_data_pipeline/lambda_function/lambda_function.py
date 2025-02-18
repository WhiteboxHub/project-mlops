import json
import boto3

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


# import json
# import boto3

# # Initialize AWS clients
# s3 = boto3.client("s3")
# ecs_client = boto3.client("ecs")

# # Define ECS Cluster and Task
# CLUSTER_NAME = "MLOpsCluster_aka"
# TASK_DEFINITION = "MLOpsTask_aka"

# def is_file_processed(bucket, key):
#     """Check if the file has already been processed using S3 metadata."""
#     try:
#         response = s3.head_object(Bucket=bucket, Key=key)
#         return 'processed' in response['Metadata']
#     except Exception as e:
#         print(f"Error checking metadata for {key}: {e}")
#         return False

# def mark_file_as_processed(bucket, key):
#     """Mark the file as processed using S3 metadata."""
#     try:
#         s3.copy_object(
#             Bucket=bucket,
#             CopySource={'Bucket': bucket, 'Key': key},
#             Key=key,
#             Metadata={'processed': 'true'},
#             MetadataDirective='REPLACE'
#         )
#         print(f"File {key} marked as processed.")
#     except Exception as e:
#         print(f"Error marking file {key} as processed: {e}")

# def lambda_handler(event, context):
#     print("Event received:", json.dumps(event))

#     for record in event['Records']:
#         bucket = record['s3']['bucket']['name']
#         key = record['s3']['object']['key']

#         # Check if the file has already been processed
#         if is_file_processed(bucket, key):
#             print(f"Skipping {key}, already processed.")
#             return {"statusCode": 200, "body": f"File {key} already processed."}

#         # Trigger ECS Task
#         response = ecs_client.run_task(
#             cluster=CLUSTER_NAME,
#             launchType="FARGATE",
#             taskDefinition=TASK_DEFINITION,
#         )

#         print("ECS Task triggered:", response)

#         # Mark file as processed
#         mark_file_as_processed(bucket, key)

#     return {"statusCode": 200, "body": "ECS Task Started Successfully"}

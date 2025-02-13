#!/bin/bash

set +e  # Continue execution even if errors occur

CONFIG_FILE=".env"

if [ -f "$CONFIG_FILE" ]; then
    echo "Loading configuration from $CONFIG_FILE..."
    source "$CONFIG_FILE"
else
    echo "Error: Configuration file $CONFIG_FILE not found!"
    exit 1
fi

echo "🚀 Starting Cleanup of AWS MLOps Data Pipeline Resources..."

## 🔟 Delete CloudWatch Log Group
echo "🗑️ Deleting CloudWatch Log Group: $LOG_GROUP_NAME..."
aws logs delete-log-group --log-group-name $LOG_GROUP_NAME || true
echo "✅ CloudWatch Log Group deleted (or already removed)."

## 9️⃣ Remove S3 Trigger Permissions from Lambda
echo "🚫 Removing S3 trigger permissions from Lambda..."
aws lambda remove-permission --function-name $LAMBDA_FUNCTION_NAME --statement-id AllowS3Trigger || true
echo "✅ S3 trigger permissions removed."

## 8️⃣ Remove S3 Event Notification
echo "📤 Removing S3 Event Notification..."
aws s3api put-bucket-notification-configuration --bucket $BUCKET_NAME --notification-configuration '{}' || true
echo "✅ S3 Event Notification removed."

## 7️⃣ Delete Lambda Function
echo "🗑️ Deleting Lambda function: $LAMBDA_FUNCTION_NAME..."
aws lambda delete-function --function-name $LAMBDA_FUNCTION_NAME || true
echo "✅ Lambda function deleted."

## 6️⃣ Delete IAM Policy for Lambda
echo "🚫 Deleting IAM Policy for Lambda..."
aws iam delete-role-policy --role-name $ROLE_NAME --policy-name "LambdaExecutionPolicy" || true
echo "✅ Lambda IAM Policy deleted."

## 5️⃣ Deregister ECS Task Definition
echo "📌 Deregistering ECS Task Definition..."
TASK_REVISION=$(aws ecs list-task-definitions --family-prefix $ECS_TASK_DEFINITION --query "taskDefinitionArns[-1]" --output text || true)
aws ecs deregister-task-definition --task-definition $TASK_REVISION || true
echo "✅ ECS Task Definition deregistered."

## 4️⃣ Delete ECR Repository and Images
echo "🗑️ Deleting ECR Repository and images..."
aws ecr delete-repository --repository-name $ECR_REPOSITORY_NAME --force || true
echo "✅ ECR Repository deleted."

## 3️⃣ Delete ECS Cluster
echo "🚫 Deleting ECS Cluster: $ECS_CLUSTER_NAME..."
aws ecs delete-cluster --cluster $ECS_CLUSTER_NAME || true
echo "✅ ECS Cluster deleted."

## 2️⃣ Detach and Delete IAM Role
echo "📌 Detaching IAM Policies from Role..."
aws iam detach-role-policy --role-name $ROLE_NAME --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy || true
aws iam detach-role-policy --role-name $ROLE_NAME --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess || true
echo "✅ IAM Policies detached."

echo "🗑️ Deleting IAM Role: $ROLE_NAME..."
aws iam delete-role --role-name $ROLE_NAME || true
echo "✅ IAM Role deleted."

## 1️⃣ Delete S3 Bucket
echo "🗑️ Deleting S3 Bucket: $BUCKET_NAME..."
aws s3 rm s3://$BUCKET_NAME --recursive || true
aws s3 rb s3://$BUCKET_NAME --force || true
echo "✅ S3 Bucket deleted."

echo "✅ AWS MLOps Data Pipeline Cleanup Complete! 🚀"

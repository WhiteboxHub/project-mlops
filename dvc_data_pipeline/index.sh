#!/bin/bash

set -e  # Exit on error

# Load configuration from config.env
CONFIG_FILE=".env"

if [ -f "$CONFIG_FILE" ]; then
    echo "Loading configuration from $CONFIG_FILE..."
    source "$CONFIG_FILE"
else
    echo "Error: Configuration file $CONFIG_FILE not found!"
    exit 1
fi

echo "Creating AWS MLOps Data Pipeline Resources..."

## 1️⃣ Create S3 Bucket for Raw & Processed Data
echo "Creating S3 Bucket: $BUCKET_NAME..."
aws s3 mb s3://$BUCKET_NAME
echo "S3 Bucket created."

## 2️⃣ Create IAM Role for ECS Task Execution
echo "Creating IAM Role: $ROLE_NAME..."
aws iam create-role --role-name $ROLE_NAME --assume-role-policy-document file://aws_policies/trust-policy.json

# Attach required policies
aws iam attach-role-policy --role-name $ROLE_NAME --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
aws iam attach-role-policy --role-name $ROLE_NAME --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
echo "IAM Role created."
echo "IAM Role created."




echo "Creating CloudWatch Log Group..."


# Fix: Remove Windows-style paths if accidentally included
LOG_GROUP_NAME=$(basename "$LOG_GROUP_NAME")

# Fix: Ensure LOG_GROUP_NAME is valid (removes invalid characters)
LOG_GROUP_NAME=$(echo "$LOG_GROUP_NAME" | sed 's/[^A-Za-z0-9._/#-]//g')

echo "Using Log Group Name: $LOG_GROUP_NAME"

# Check if the log group already exists
LOG_GROUP_EXISTS=$(aws logs describe-log-groups --log-group-name-prefix "$LOG_GROUP_NAME" --query "logGroups[*].logGroupName" --output text || echo "")

if [[ "$LOG_GROUP_EXISTS" == "$LOG_GROUP_NAME" ]]; then
    echo "Log group '$LOG_GROUP_NAME' already exists. Skipping creation."
else
    # Create log group if it does not exist
    echo "Creating CloudWatch Log Group: $LOG_GROUP_NAME..."
    aws logs create-log-group --log-group-name "$LOG_GROUP_NAME"
    echo "Log Group created successfully."
fi





## 3️⃣ Create ECS Cluster
echo "Creating ECS Cluster: $ECS_CLUSTER_NAME..."
aws ecs create-cluster --cluster-name $ECS_CLUSTER_NAME
echo "ECS Cluster created."

## 4️⃣ Create ECR Repository for Docker Images
echo "Creating ECR Repository: $ECR_REPOSITORY_NAME..."
aws ecr create-repository --repository-name $ECR_REPOSITORY_NAME
echo "ECR Repository created."

## 5️⃣ Push Docker Image to ECR
echo "Pushing Docker Image to ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
docker build -t $ECR_REPOSITORY_NAME .
docker tag $ECR_REPOSITORY_NAME:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY_NAME:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY_NAME:latest
echo "Docker image pushed."

## 6️⃣ Create ECS Task Definition
echo "Creating ECS Task Definition..."

aws ecs register-task-definition --family "$ECS_TASK_DEFINITION" \
  --execution-role-arn "arn:aws:iam::$AWS_ACCOUNT_ID:role/$ROLE_NAME" \
  --network-mode awsvpc \
  --requires-compatibilities FARGATE \
  --memory "512" \
  --cpu "256" \
  --container-definitions "[
    {
      \"name\": \"data-cleaning-container\",
      \"image\": \"$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY_NAME:latest\",
      \"memory\": 512,
      \"cpu\": 256,
      \"essential\": true,
      \"logConfiguration\": {
        \"logDriver\": \"awslogs\",
        \"options\": {
          \"awslogs-group\": \"$LOG_GROUP_NAME\",
          \"awslogs-region\": \"$AWS_REGION\",
          \"awslogs-stream-prefix\": \"ecs\"
        }
      }
    }
  ]"

echo "ECS Task Definition created."

# Set your VPC ID (or retrieve dynamically)
VPC_ID=$(aws ec2 describe-vpcs --query "Vpcs[0].VpcId" --output text)

# Get the first available Subnet ID in the VPC
SUBNET_ID=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" --query "Subnets[0].SubnetId" --output text)

# Get the first available Security Group ID in the VPC
SECURITY_GROUP_ID=$(aws ec2 describe-security-groups --filters "Name=vpc-id,Values=$VPC_ID" --query "SecurityGroups[0].GroupId" --output text)

# Check if the values were retrieved successfully
if [[ -z "$SUBNET_ID" || -z "$SECURITY_GROUP_ID" ]]; then
    echo "Error: Could not fetch Subnet ID or Security Group ID."
    exit 1
fi

echo "Found Subnet ID: $SUBNET_ID"
echo "Found Security Group ID: $SECURITY_GROUP_ID"

# Add the retrieved values to the ECS service creation command
CMD="aws ecs create-service \
  --cluster \"\$ECS_CLUSTER_NAME\" \
  --service-name \"\$ECS_SERVICE_NAME\" \
  --task-definition \"\$ECS_TASK_DEFINITION\" \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration \"awsvpcConfiguration={subnets=[$SUBNET_ID],securityGroups=[$SECURITY_GROUP_ID],assignPublicIp='ENABLED'}\""

echo "Running Command:"
echo "$CMD"

# Execute the command
eval $CMD

## 6️⃣ Zip Lambda Function Code
echo "Zipping Lambda function..."
zip lambda_function.zip ./lambda_function/lambda_handler.py
echo "Lambda function zipped."

aws iam put-role-policy \
  --role-name "$ROLE_NAME" \
  --policy-name "LambdaExecutionPolicy" \
  --policy-document file://aws_policies/lambda_policy.json

## 7️⃣ Create Lambda Function to Trigger ECS
echo "Creating Lambda function..."
aws lambda create-function \
  --function-name "$LAMBDA_FUNCTION_NAME" \
  --runtime python3.8 \
  --role "arn:aws:iam::$AWS_ACCOUNT_ID:role/$ROLE_NAME" \
  --handler lambda_function.lambda_handler \
  --zip-file "fileb://lambda_function.zip"


echo "Lambda function created."

aws lambda add-permission \
  --function-name "$LAMBDA_FUNCTION_NAME" \
  --principal s3.amazonaws.com \
  --statement-id "AllowS3Invoke" \
  --action "lambda:InvokeFunction" \
  --source-arn "arn:aws:s3:::$BUCKET_NAME"


## 8️⃣ Set Up S3 Event Notification to Trigger Lambda
echo "Setting up S3 Event Notification..."
aws s3api put-bucket-notification-configuration --bucket $BUCKET_NAME --notification-configuration '{
  "LambdaFunctionConfigurations": [
    {
      "LambdaFunctionArn": "arn:aws:lambda:'$AWS_REGION':'$AWS_ACCOUNT_ID':function:'$LAMBDA_FUNCTION_NAME'",
      "Events": ["s3:ObjectCreated:*"],
      "Filter": {
        "Key": {
          "FilterRules": [
            {
              "Name": "prefix",
              "Value": "raw/"
            }
          ]
        }
      }
    }
  ]
}'
echo "S3 Event Notification set."

## 9️⃣ Grant S3 Trigger Permissions to Lambda
echo "Granting S3 trigger permissions to Lambda..."
aws lambda add-permission --function-name $LAMBDA_FUNCTION_NAME \
  --statement-id AllowS3Trigger \
  --action "lambda:InvokeFunction" \
  --principal "s3.amazonaws.com" \
  --source-arn arn:aws:s3:::$BUCKET_NAME \
  --source-account $AWS_ACCOUNT_ID
echo "S3 trigger permissions granted."

## 🔟 Create CloudWatch Log Group



echo "AWS MLOps Data Pipeline setup is complete! 🚀🎉"
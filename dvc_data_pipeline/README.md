# AWS MLOps Data Pipeline Setup

## Overview

This script automates the setup of an AWS MLOps data pipeline by creating necessary AWS resources such as S3, IAM roles, ECS, ECR, Lambda, and CloudWatch.

## Folder Structure

```
└── 📁dvc_data_pipeline
    └── 📁aws_policies
        └── iam-policies.json
        └── lambda_policy.json
        └── permissions-policy-template.json
        └── trust-policy.json
    └── 📁lambda_function
        └── handler.py
        └── lambda_function.py
    └── 📁pipeline
        └── 📁data_loading
            └── __init__.py
            └── clean_data.py
            └── get_s3_csv_data.py
            └── ready_data_for_training.py
            └── s3_upload_traing.py
        └── data_preprocessing.py
        └── data_validataion.py
    └── .dockerignore
    └── .env
    └── deleting_script.sh  # Deletes all created AWS resources
    └── Dockerfile
    └── dvc_setup.sh
    └── example.env
    └── index.sh  # Creates the AWS MLOps data pipeline
    └── lambda_function.zip
    └── main.py
    └── README.md
    └── requirements.txt
```

## Prerequisites

- Docker ([Installation Guide](https://docs.docker.com/get-docker/))
- An AWS account with necessary permissions
- AWS CLI installed ([Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html))
- A `.env` file with the required environment variables

## AWS CLI Configuration

To connect your AWS account using the AWS CLI, run:

```bash
aws configure
```

You will be prompted to enter the following details:

```
AWS Access Key ID [None]: YOUR_ACCESS_KEY
AWS Secret Access Key [None]: YOUR_SECRET_KEY
Default region name [None]: YOUR_AWS_REGION
Default output format [None]: json
```

This configures your AWS CLI to interact with your AWS account.

## Configuration

Create a `.env` file in the root directory and define the following variables:

```bash
AWS_REGION=<your-aws-region>
AWS_ACCOUNT_ID=<your-aws-account-id>
BUCKET_NAME=<your-s3-bucket-name>
ROLE_NAME=<your-iam-role-name>
LOG_GROUP_NAME=<your-cloudwatch-log-group>
ECS_CLUSTER_NAME=<your-ecs-cluster-name>
ECR_REPOSITORY_NAME=<your-ecr-repo-name>
ECS_TASK_DEFINITION=<your-ecs-task-definition>
ECS_SERVICE_NAME=<your-ecs-service-name>
LAMBDA_FUNCTION_NAME=<your-lambda-function-name>
```

## Script Execution

### Creating the Pipeline

Run the script using:

```bash
chmod +x index.sh
./index.sh
```

This script creates all necessary AWS resources for the pipeline.

### Deleting Resources

To delete all created resources, run:

```bash
chmod +x deleting_script.sh
./deleting_script.sh
```

This script ensures a clean teardown of the pipeline.

## Resources Created

### 1. S3 Bucket

- Creates an S3 bucket for storing raw and processed data.

### 2. IAM Role

- Creates an IAM role for ECS task execution and attaches necessary policies.

### 3. CloudWatch Log Group

- Ensures the log group exists before creation.

### 4. ECS Cluster

- Creates an ECS cluster for managing containerized applications.

### 5. ECR Repository

- Creates an ECR repository for storing Docker images.

### 6. Docker Image Deployment

- Builds and pushes a Docker image to ECR.

### 7. ECS Task Definition

- Registers an ECS task definition with the required configurations.

### 8. ECS Service

- Creates an ECS service with network configurations.

### 9. Lambda Function

- Zips and deploys a Lambda function to trigger ECS.
- Grants necessary execution permissions.

### 10. S3 Event Notification

- Configures an event notification to trigger the Lambda function on new object uploads.

## Troubleshooting

- If you encounter permission issues, verify IAM role policies and permissions.
- If the script fails, check CloudWatch logs and AWS CLI command responses.

## Conclusion

This script automates the creation of an end-to-end AWS MLOps pipeline, allowing seamless data processing and model deployment.

---




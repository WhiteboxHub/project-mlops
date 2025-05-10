import boto3
import json


ecs_client = boto3.client('ecs')

def lambda_handler(event,context):
    print("Received event:",json.dumps(event))

    response = ecs_client.run_task(
        cluster = "my-ecs-cluster",
        launchType="FARGATE",
        taskDefinition = "my-ecs-task:1",
        networkConfiguration = {
            "awsvpcConfiguration":{
                "subnets":[
                            "subnet-07373ed7972da8f3d",
                            "subnet-09f14006d3a1b5bdd",
                            "subnet-0b14fc3c69dfcdbc2",
                            "subnet-0ca74b060d32653ce",
                            "subnet-069e24424811e858f",
                            "subnet-0afe83087dfda65f0"
                            ],
                "securityGroups":[
                                "sg-043a09fc174d48942",
                                "sg-06867dab2a24649eb",
                                "sg-07d237cf431864a0e",
                                "sg-07abbff5e012d3aec",
                                "sg-08ecc55791c11a820",
                                "sg-025f3853f7a491e50",
                                "sg-0181310c963a1c7f9",
                                "sg-06fe7be88c4669492",
                                "sg-09c76a3bdd9f9222e",
                                "sg-0e4601520be3390d5",
                                "sg-06085ded0d372fd45",
                                "sg-091dec4a1087c51be",
                                "sg-09d8e4e19bcdcacd5"
                            ],

                "assignPublicIp":"ENABLED"
            }
        }
        
    )

    print("Task Started:",response)
    return {"Status":"Task started"}
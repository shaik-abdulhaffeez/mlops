import boto3
import json

def create_state_machine(role_arn, bucket, prefix, local_file):
    stepfunctions = boto3.client('stepfunctions')

    definition = {
        "Comment": "A state machine for MLOps with SageMaker",
        "StartAt": "DataPreparation",
        "States": {
            "DataPreparation": {
                "Type": "Task",
                "Resource": "arn:aws:states:::lambda:invoke",
                "Parameters": {
                    "FunctionName": "MLOpsLambdaFunction",
                    "Payload": {
                        "action": "data_preparation",
                        "bucket": bucket,
                        "prefix": prefix,
                        "local_file": local_file
                    }
                },
                "Next": "ModelTraining"
            },
            "ModelTraining": {
                "Type": "Task",
                "Resource": "arn:aws:states:::lambda:invoke",
                "Parameters": {
                    "FunctionName": "MLOpsLambdaFunction",
                    "Payload": {
                        "action": "model_training",
                        "bucket": bucket,
                        "prefix": prefix,
                        "role": role_arn
                    }
                },
                "Next": "ModelDeployment"
            },
            "ModelDeployment": {
                "Type": "Task",
                "Resource": "arn:aws:states:::lambda:invoke",
                "Parameters": {
                    "FunctionName": "MLOpsLambdaFunction",
                    "Payload": {
                        "action": "model_deployment",
                        "model_arn": "$.Payload.model_arn"
                    }
                },
                "Next": "ModelMonitoring"
            },
            "ModelMonitoring": {
                "Type": "Task",
                "Resource": "arn:aws:states:::lambda:invoke",
                "Parameters": {
                    "FunctionName": "MLOpsLambdaFunction",
                    "Payload": {
                        "action": "model_monitoring",
                        "endpoint_name": "$.Payload.endpoint_name"
                    }
                },
                "Next": "CICDPipeline"
            },
            "CICDPipeline": {
                "Type": "Task",
                "Resource": "arn:aws:states:::lambda:invoke",
                "Parameters": {
                    "FunctionName": "MLOpsLambdaFunction",
                    "Payload": {
                        "action": "cicd_pipeline",
                        "bucket": bucket,
                        "role": role_arn
                    }
                },
                "End": True
            }
        }
    }

    response = stepfunctions.create_state_machine(
        name='SageMakerMLOpsStateMachine',
        definition=json.dumps(definition),
        roleArn=role_arn
    )

    print(f'State machine created: {response["stateMachineArn"]}')
    return response["stateMachineArn"]

def execute_state_machine(state_machine_arn):
    stepfunctions = boto3.client('stepfunctions')

    response = stepfunctions.start_execution(
        stateMachineArn=state_machine_arn,
        input='{}'
    )

    print(f'Execution started: {response["executionArn"]}')

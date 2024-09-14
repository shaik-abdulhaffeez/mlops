import boto3
import sagemaker
from sagemaker import get_execution_role
from data.data_preparation import prepare_data
from models.model_training import train_model
from models.model_deployment import deploy_model
from monitoring.model_monitoring import monitor_model
from cicd.cicd_pipeline import create_pipeline

def lambda_handler(event, context):
    action = event.get('action')
    bucket = event.get('bucket')
    prefix = event.get('prefix')
    local_file = event.get('local_file')
    role = event.get('role')

    if action == 'data_preparation':
        prepare_data(bucket, prefix, local_file)
        return {
            'statusCode': 200,
            'body': 'Data preparation completed'
        }

    elif action == 'model_training':
        model = train_model(bucket, prefix, role)
        return {
            'statusCode': 200,
            'body': 'Model training completed',
            'model_arn': model.model_data
        }

    elif action == 'model_deployment':
        model_arn = event.get('model_arn')
        model = sagemaker.estimator.Estimator.attach(model_arn)
        predictor = deploy_model(model)
        return {
            'statusCode': 200,
            'body': 'Model deployment completed',
            'endpoint_name': predictor.endpoint_name
        }

    elif action == 'model_monitoring':
        endpoint_name = event.get('endpoint_name')
        monitor_model(endpoint_name)
        return {
            'statusCode': 200,
            'body': 'Model monitoring completed'
        }

    elif action == 'cicd_pipeline':
        create_pipeline(bucket, role)
        return {
            'statusCode': 200,
            'body': 'CI/CD pipeline created'
        }

    else:
        return {
            'statusCode': 400,
            'body': 'Invalid action'
        }

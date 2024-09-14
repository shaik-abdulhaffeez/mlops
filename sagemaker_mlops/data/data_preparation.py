import boto3
import sagemaker
from sagemaker import get_execution_role

def prepare_data(bucket, prefix, local_file):
    sagemaker_session = sagemaker.Session()
    role = get_execution_role()

    s3 = boto3.client('s3')
    s3.upload_file(local_file, bucket, f'{prefix}/data.csv')

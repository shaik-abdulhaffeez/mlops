import boto3
import sagemaker
from sagemaker.amazon.amazon_estimator import get_image_uri

def train_model(bucket, prefix, role):
    container = get_image_uri(boto3.Session().region_name, 'xgboost')

    xgboost = sagemaker.estimator.Estimator(container,
                                            role,
                                            train_instance_count=1,
                                            train_instance_type='ml.m4.xlarge',
                                            output_path=f's3://{bucket}/{prefix}/output',
                                            sagemaker_session=sagemaker.Session())

    xgboost.set_hyperparameters(objective='reg:squarederror', num_round=100)

    train_data = sagemaker.inputs.TrainingInput(s3_data=f's3://{bucket}/{prefix}/data.csv', content_type='csv')

    xgboost.fit({'train': train_data})

    return xgboost

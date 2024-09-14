import time
import boto3

def monitor_model(predictor):
    cloudwatch = boto3.client('cloudwatch')

    metrics = [
        'Invocations',
        'ModelLatency',
        'OverheadLatency',
        'ResponseLatency'
    ]

    for metric in metrics:
        response = cloudwatch.get_metric_statistics(
            Namespace='AWS/SageMaker',
            MetricName=metric,
            Dimensions=[
                {
                    'Name': 'EndpointName',
                    'Value': predictor.endpoint_name
                }
            ],
            StartTime=time.time() - 60 * 60,  # Last hour
            EndTime=time.time(),
            Period=60,
            Statistics=['Average']
        )
        print(f'{metric}: {response["Datapoints"]}')

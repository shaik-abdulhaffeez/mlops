import boto3

def create_pipeline(bucket, role):
    codepipeline = boto3.client('codepipeline')

    pipeline = {
        'pipeline': {
            'name': 'SageMakerPipeline',
            'roleArn': role,
            'stages': [
                {
                    'name': 'Source',
                    'actions': [
                        {
                            'name': 'Source',
                            'actionTypeId': {
                                'category': 'Source',
                                'owner': 'AWS',
                                'provider': 'S3',
                                'version': '1'
                            },
                            'runOrder': 1,
                            'configuration': {
                                'S3Bucket': bucket,
                                'S3ObjectKey': 'pipeline.zip'
                            },
                            'outputArtifacts': [
                                {
                                    'name': 'SourceArtifact'
                                }
                            ],
                            'inputArtifacts': [],
                            'region': boto3.Session().region_name
                        }
                    ]
                },
                {
                    'name': 'Build',
                    'actions': [
                        {
                            'name': 'Build',
                            'actionTypeId': {
                                'category': 'Build',
                                'owner': 'AWS',
                                'provider': 'CodeBuild',
                                'version': '1'
                            },
                            'runOrder': 1,
                            'configuration': {
                                'ProjectName': 'SageMakerBuildProject'
                            },
                            'outputArtifacts': [
                                {
                                    'name': 'BuildArtifact'
                                }
                            ],
                            'inputArtifacts': [
                                {
                                    'name': 'SourceArtifact'
                                }
                            ],
                            'region': boto3.Session().region_name
                        }
                    ]
                },
                {
                    'name': 'Deploy',
                    'actions': [
                        {
                            'name': 'Deploy',
                            'actionTypeId': {
                                'category': 'Deploy',
                                'owner': 'AWS',
                                'provider': 'SageMaker',
                                'version': '1'
                            },
                            'runOrder': 1,
                            'configuration': {
                                'ProjectName': 'SageMakerDeployProject'
                            },
                            'outputArtifacts': [],
                            'inputArtifacts': [
                                {
                                    'name': 'BuildArtifact'
                                }
                            ],
                            'region': boto3.Session().region_name
                        }
                    ]
                }
            ],
            'artifactStore': {
                'type': 'S3',
                'location': bucket
            }
        }
    }

    response = codepipeline.create_pipeline(**pipeline)
    print(f'Pipeline created: {response["pipeline"]["name"]}')

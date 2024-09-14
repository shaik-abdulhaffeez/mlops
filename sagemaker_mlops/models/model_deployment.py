def deploy_model(model):
    predictor = model.deploy(initial_instance_count=1, instance_type='ml.m4.xlarge')
    return predictor

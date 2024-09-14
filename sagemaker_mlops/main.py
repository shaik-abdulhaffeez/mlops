import logging
from orchestration.step_functions import create_state_machine, execute_state_machine

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    bucket = 'your-s3-bucket'
    prefix = 'sagemaker/data'
    local_file = 'local_data.csv'
    role = 'your-sagemaker-role'

    # Create state machine
    state_machine_arn = create_state_machine(role, bucket, prefix, local_file)

    # Execute state machine
    execute_state_machine(state_machine_arn)

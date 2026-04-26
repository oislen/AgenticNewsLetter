import boto3
import json
import os

def get_secrets():
    """
    Retrieves secrets from AWS Secrets Manager using the ARN provided in the environment variable.

    Parameters:
    -----------
    None

    Returns:
    --------
    dict
        A dictionary containing the secrets retrieved from AWS Secrets Manager.
    
    Example:
    --------
    ```
    secrets = get_secrets()
    ``` 
    """
    secret_arn = os.getenv("SECRET_ARN")
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=secret_arn)
    return json.loads(response['SecretString'])
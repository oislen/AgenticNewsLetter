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

def get_test_secrets(cons):
    """
    Retrieves secrets from local test environment.

    Parameters:
    -----------
    cons :
        The constants python module

    Returns:
    --------
    dict
        A dictionary containing the retrieved test secrets.
    
    Example:
    --------
    ```
    secrets = get_secrets()
    """
    # define get test secret function
    def get_test_secret(fpath):
        with open(fpath, "r") as file:
            secret = file.readline()
        return secret
    # set missing defaults
    tavily_secret = None
    sender_email_username = None
    sender_email_password = None
    receiver_email_username = None
    # retrieve test secrets
    if os.path.exists(cons.tavily_api_fpath):
        tavily_secret = get_test_secret(cons.tavily_api_fpath)
    if os.path.exists(cons.sender_email_username_fpath):
        sender_email_username = get_test_secret(cons.sender_email_username_fpath)
    if os.path.exists(cons.sender_email_password_fpath):
        sender_email_password = get_test_secret(cons.sender_email_password_fpath)
    if os.path.exists(cons.receiver_email_username_fpath):
        receiver_email_username = get_test_secret(cons.receiver_email_username_fpath)
    secrets = {
        "TAVILY_API_KEY":tavily_secret,
        "SENDER_EMAIL":sender_email_username,
        "SENDER_PASSWORD":sender_email_password,
        "RECEIVER_EMAIL":receiver_email_username,
        }
    return secrets
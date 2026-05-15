import boto3
import json
import os
import cons

def bedrock_client(region_name="eu-west-1"):
    """
    Initializes a boto3 client for AWS Bedrock Runtime using temporary credentials stored in a JSON file.

    Parameters:
    -----------
    region_name : str
        The AWS region where the Bedrock Runtime service is hosted. Default is "eu-west-1".
    
    Returns:
    --------
    boto3.client
        A boto3 client object for interacting with AWS Bedrock Runtime.

    Example:
    --------
    ```
    bedrock_runtime = bedrock_client(region_name="eu-west-1")
    ```
    """
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID", None)
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY", None)
    aws_session_token = os.environ.get("AWS_SESSION_TOKEN", None)
    # load aws configs
    if aws_access_key_id is None and aws_secret_access_key is None and aws_session_token is None and os.path.exists(cons.session_token_fpath):
        with open(cons.session_token_fpath, 'r') as j:
            aws_config = json.loads(j.read())
        aws_access_key_id=aws_config['aws_access_key_id']
        aws_secret_access_key=aws_config['aws_secret_access_key']
        aws_session_token=aws_config['aws_session_token']
    # create boto3 session with temporary credentials
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token
    )
    # Initialize the Bedrock Runtime client
    bedrock_runtime = session.client(
        service_name="bedrock-runtime",
        region_name=region_name
    )
    return bedrock_runtime
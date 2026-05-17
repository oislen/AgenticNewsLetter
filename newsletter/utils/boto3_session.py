import os
import boto3

def boto3_session():
    """
    Creates a boto3 session using temporary credentials stored in environment variables.
    
    Parameters:
    -----------
    None
    
    Returns:
    --------
    boto3.Session
        A boto3 session object initialized with temporary credentials if available, otherwise returns the default boto3 module.
    
    Example:
    --------
    ```
    session = boto3_session()
    ```
    """
    # create boto3 session with temporary credentials
    if ("AWS_ACCESS_KEY_ID" in os.environ) and ("AWS_SECRET_ACCESS_KEY" in os.environ) and ("AWS_SESSION_TOKEN" in os.environ):
        session = boto3.Session(
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
            aws_session_token=os.environ["AWS_SESSION_TOKEN"]
        )
    else:
        session=boto3
    return session
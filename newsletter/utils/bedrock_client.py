import boto3
import json
import os
import cons

def bedrock_client(session, region_name="eu-west-1"):
    """
    Initializes a boto3 client for AWS Bedrock Runtime using temporary credentials stored in a JSON file.

    Parameters:
    -----------
    session : boto3.Session
        A boto3 session object initialized with temporary credentials.
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
    # Initialize the Bedrock Runtime client
    bedrock_runtime = session.client(
        service_name="bedrock-runtime",
        region_name=region_name
    )
    return bedrock_runtime
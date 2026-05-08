#!/usr/bin/env python3 app.py
import os
import sys
import logging

import aws_cdk as cdk

root_dir = os.getcwd().split("AgenticNewsLetter")[0]
sys.path.append(root_dir)
sys.path.append(os.path.join(root_dir, "AgenticNewsLetter"))

from aws.cdk.stacks.NewsletterStack import NewsletterStack

# set up logging
lgr = logging.getLogger()
lgr.setLevel(logging.INFO)

# Get AWS account and region from environment variables (set by CDK CLI)
account = os.getenv("CDK_DEFAULT_ACCOUNT")
region = os.getenv("CDK_DEFAULT_REGION")
initial_run = os.getenv("CDK_INITIAL_RUN", False).strip().lower() == True

logging.info(f"account: {account}")
logging.info(f"region: {region}")
logging.info(f"initial_run: {initial_run}")

# Define deployment environment (account and region)
deployment_env = cdk.Environment(
    account=account,
    region=region,
)

# Create CDK app and stack
app = cdk.App()

# First Feature Stack
newsletter_stack = NewsletterStack(
    scope=app,
    construct_id="NewsletterFeatureStack",
    initial_run=initial_run,
    env=deployment_env
)

app.synth()


import os
import logging
from dotenv import load_dotenv
from datetime import datetime

import cons
from graph import builder
from utils import random_inputs, get_secrets, boto3_session

def lambda_handler(event, context):
    # set up logging
    lgr = logging.getLogger()
    lgr.setLevel(logging.INFO)

    logging.info("Loading environment ...")
    # load .env variables
    load_dotenv()
    # create boto3 session
    session = boto3_session()
    # create service clients
    secretsClient = session.client(service_name="secretsmanager", region_name=os.environ["AWS_REGION"])
    bedrockClient = session.client(service_name="bedrock-runtime", region_name=os.environ["AWS_REGION"])
    # compile graph
    graph = builder.compile()
    # generate random inputs
    inputs = random_inputs(seed=int(datetime.now().strftime("%Y%m%d")))
    # set graph state
    state = {
        "topic": inputs['topic'],
        "subtopic": inputs['subtopic'],
        "style": inputs['style'],
        "steps_taken": [],
        "bedrock_client": bedrockClient,
        "bedrock_model_id": os.environ["BEDROCK_MODEL_ID"]
    }
    configurable = {
        "configurable":{
            "TAVILY_API_KEY":get_secrets(secretsClient, os.environ["TAVILY_API_KEY_ARN"]),
            "SENDER_EMAIL":os.environ["SENDER_EMAIL"],
            "SENDER_PASSWORD":get_secrets(secretsClient,os.environ["SENDER_PASSWORD_ARN"]),
            "RECEIVER_EMAIL":os.environ["RECEIVER_EMAIL"],
        }
    }
    # invoke graph
    graph.invoke(state, config=configurable)
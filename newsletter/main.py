
import os
import sys
from dotenv import load_dotenv
from datetime import datetime

import cons
from graph import builder
from utils import random_inputs, get_secrets, boto3_session

if __name__ == "__main__":
    # load .env variables
    load_dotenv()
    # create boto3 session
    session = boto3_session()
    # create service clients
    secretsClient = session.client(service_name="secretsmanager")
    bedrockClient = session.client(service_name="bedrock-runtime")
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
            "TAVILY_API_KEY":get_secrets(secretsClient, os.environ["TAVILY_API_KEY"]),
            "SENDER_EMAIL":os.environ["SENDER_EMAIL"],
            "SENDER_PASSWORD":get_secrets(secretsClient,os.environ["SENDER_PASSWORD"]),
            "RECEIVER_EMAIL":os.environ["RECEIVER_EMAIL"],
        }
    }
    # invoke graph
    graph.invoke(state, config=configurable)
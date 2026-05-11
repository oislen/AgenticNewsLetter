
import os
import sys

import cons
from graph import builder
from utils import random_inputs, get_secrets, get_test_secrets

if __name__ == "__main__":
    graph = builder.compile()

    # generate random inputs
    inputs = random_inputs()
    if cons.localTestEnv:
        secrets = get_test_secrets(cons)
    else:
        secrets = get_secrets()
    # assign secrets to runtime environment
    os.environ["TAVILY_API_KEY"] = secrets['TAVILY_API_KEY']
    os.environ["SENDER_EMAIL"] = secrets['SENDER_EMAIL']
    os.environ["SENDER_PASSWORD"] = secrets['SENDER_PASSWORD']
    breakpoint()

    # Change 'style' here to switch the newsletter's behavior
    graph.invoke({
        "topic": inputs['topic'],
        "subtopic": inputs['subtopic'],
        "style": inputs['style'],
        "steps_taken": []
    })
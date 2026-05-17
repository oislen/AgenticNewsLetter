
import os
import sys
from dotenv import load_dotenv
from datetime import datetime

import cons
from graph import builder
from utils import random_inputs

if __name__ == "__main__":

    # load .env variables
    load_dotenv()
    # compile graph
    graph = builder.compile()
    # generate random inputs
    inputs = random_inputs(seed=int(datetime.now().strftime("%Y%m%d")))
    # Change 'style' here to switch the newsletter's behavior
    graph.invoke({
        "topic": inputs['topic'],
        "subtopic": inputs['subtopic'],
        "style": inputs['style'],
        "steps_taken": []
    })
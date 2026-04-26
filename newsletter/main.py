
import os
from graph import builder
from utils import random_inputs, get_secrets

if __name__ == "__main__":
    graph = builder.compile()

    # generate random inputs
    inputs = random_inputs()

    secrets = get_secrets()
    os.environ["TAVILY_API_KEY"] = secrets['TAVILY_API_KEY']
    
    # Change 'style' here to switch the newsletter's behavior
    graph.invoke({
        "topic": inputs['topic'], 
        "subtopic": inputs['subtopic'],
        "style": inputs['style'],
        "steps_taken": []
    })
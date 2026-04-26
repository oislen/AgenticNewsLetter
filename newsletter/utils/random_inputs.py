
import random

from utils import topics, style_guides

def random_inputs():
    """
    Generate random inputs for the newsletter graph. This function randomly selects a topic, subtopic, and style from the predefined lists in utils.

    Parameters:
    -----------
    None

    Returns:
    --------
    dict
        A dictionary containing randomly selected 'topic', 'subtopic', and 'style' for the newsletter.
    
    Example:
    --------
    ```
    inputs = random_inputs()
    ```
    """
    selected_topic = random.choice(list(topics.keys()))
    select_subtopic = random.choice(topics[selected_topic])
    select_style = random.choice(list(style_guides.keys()))
    inputs = {"topic": selected_topic, "subtopic": select_subtopic, "style": select_style,}
    return inputs
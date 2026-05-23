
import random

from utils import topics, style_guides

def random_inputs(seed=None):
    """
    Generate random inputs for the newsletter graph. This function randomly selects a topic, subtopic, and style from the predefined lists in utils.

    Parameters:
    -----------
    seed : int
        A random seed to set for reproducibility, default is None

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
    if seed is not None:
        random.seed(a=seed)
    selected_topic = random.choice(list(topics.keys()))
    selected_subtopic = random.choice(topics[selected_topic])
    selected_style = random.choice(list(style_guides.keys()))
    inputs = {"topic": selected_topic, "subtopic": selected_subtopic, "style": selected_style}
    return inputs
import os
import sys
import unittest

NEWSLETTER_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if NEWSLETTER_DIR not in sys.path:
    sys.path.insert(0, NEWSLETTER_DIR)

from utils.random_inputs import random_inputs
from utils.topics import topics
from utils.style_guides import style_guides


class TestRandomInputs(unittest.TestCase):

    def test_random_inputs_returns_expected_keys(self):
        result = random_inputs(seed=42)
        self.assertIn("topic", result)
        self.assertIn("subtopic", result)
        self.assertIn("style", result)

    def test_random_inputs_returns_values_from_known_lists(self):
        result = random_inputs(seed=42)
        self.assertIn(result["topic"], topics.keys())
        self.assertIn(result["subtopic"], topics[result["topic"]])
        self.assertIn(result["style"], style_guides.keys())

    def test_random_inputs_is_reproducible_with_seed(self):
        a = random_inputs(seed=123)
        b = random_inputs(seed=123)
        self.assertEqual(a, b)

    def test_random_inputs_different_seeds_can_differ(self):
        seen = {tuple(random_inputs(seed=s).values()) for s in range(50)}
        self.assertGreater(len(seen), 1)

    def test_random_inputs_without_seed_runs(self):
        result = random_inputs()
        self.assertIn("topic", result)
        self.assertIn("subtopic", result)
        self.assertIn("style", result)


if __name__ == "__main__":
    unittest.main()

import os
import sys
import unittest

sys.path.append(os.path.join(os.getcwd(), "newsletter"))

NEWSLETTER_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if NEWSLETTER_DIR not in sys.path:
    sys.path.insert(0, NEWSLETTER_DIR)

from utils.style_guides import style_guides


class TestStyleGuides(unittest.TestCase):

    def test_style_guides_is_dict(self):
        self.assertIsInstance(style_guides, dict)

    def test_style_guides_contains_expected_styles(self):
        for key in ("academic", "ELI5", "tutorial"):
            self.assertIn(key, style_guides)

    def test_style_guide_values_are_non_empty_strings(self):
        for key, value in style_guides.items():
            self.assertIsInstance(value, str, f"value for {key} is not str")
            self.assertGreater(len(value), 0, f"value for {key} is empty")


if __name__ == "__main__":
    unittest.main()

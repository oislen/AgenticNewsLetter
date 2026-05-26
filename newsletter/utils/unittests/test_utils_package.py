import os
import sys
import unittest

sys.path.append(os.path.join(os.getcwd(), "newsletter"))

NEWSLETTER_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if NEWSLETTER_DIR not in sys.path:
    sys.path.insert(0, NEWSLETTER_DIR)


class TestUtilsPackage(unittest.TestCase):

    def test_utils_exports(self):
        from utils import (
            bedrock_client,
            style_guides,
            topics,
            random_inputs,
            get_secrets,
            get_test_secrets,
            boto3_session,
        )

        self.assertTrue(callable(bedrock_client))
        self.assertTrue(callable(random_inputs))
        self.assertTrue(callable(get_secrets))
        self.assertTrue(callable(get_test_secrets))
        self.assertTrue(callable(boto3_session))
        self.assertIsInstance(style_guides, dict)
        self.assertIsInstance(topics, dict)


if __name__ == "__main__":
    unittest.main()

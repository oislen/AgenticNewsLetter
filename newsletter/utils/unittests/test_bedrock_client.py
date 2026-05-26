import os
import sys
import unittest
from unittest.mock import MagicMock

NEWSLETTER_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if NEWSLETTER_DIR not in sys.path:
    sys.path.insert(0, NEWSLETTER_DIR)

from utils.bedrock_client import bedrock_client


class TestBedrockClient(unittest.TestCase):

    def test_bedrock_client_uses_default_region(self):
        session = MagicMock()
        fake_client = MagicMock(name="bedrock-runtime-client")
        session.client.return_value = fake_client

        result = bedrock_client(session)

        session.client.assert_called_once_with(
            service_name="bedrock-runtime", region_name="eu-west-1"
        )
        self.assertIs(result, fake_client)

    def test_bedrock_client_accepts_custom_region(self):
        session = MagicMock()
        fake_client = MagicMock(name="bedrock-runtime-client")
        session.client.return_value = fake_client

        result = bedrock_client(session, region_name="us-east-1")

        session.client.assert_called_once_with(
            service_name="bedrock-runtime", region_name="us-east-1"
        )
        self.assertIs(result, fake_client)


if __name__ == "__main__":
    unittest.main()

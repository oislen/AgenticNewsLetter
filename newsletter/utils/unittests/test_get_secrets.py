import os
import sys
import json
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock

NEWSLETTER_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if NEWSLETTER_DIR not in sys.path:
    sys.path.insert(0, NEWSLETTER_DIR)

from utils.get_secrets import get_secrets, get_test_secrets


class TestGetSecrets(unittest.TestCase):

    def test_get_secrets_returns_first_value_from_secret_string(self):
        secrets_client = MagicMock()
        secrets_client.get_secret_value.return_value = {
            "SecretString": json.dumps({"TAVILY_API_KEY": "abc123"})
        }

        result = get_secrets(secrets_client, "arn:aws:secretsmanager:eu-west-1:1:secret:tavily")

        secrets_client.get_secret_value.assert_called_once_with(
            SecretId="arn:aws:secretsmanager:eu-west-1:1:secret:tavily"
        )
        self.assertEqual(result, "abc123")

    def test_get_secrets_with_multiple_keys_returns_first(self):
        secrets_client = MagicMock()
        secrets_client.get_secret_value.return_value = {
            "SecretString": json.dumps({"first": "one", "second": "two"})
        }

        result = get_secrets(secrets_client, "arn")
        # `list(dict.values())[0]` — Python 3.7+ preserves insertion order
        self.assertEqual(result, "one")


class TestGetTestSecrets(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def _write(self, name, contents):
        fpath = os.path.join(self.tmp.name, name)
        with open(fpath, "w") as f:
            f.write(contents)
        return fpath

    def test_get_test_secrets_reads_all_present_files(self):
        cons = SimpleNamespace(
            tavily_api_fpath=self._write("tavily", "tav-key"),
            sender_email_username_fpath=self._write("sender_user", "sender@example.com"),
            sender_email_password_fpath=self._write("sender_pw", "pwd"),
            receiver_email_username_fpath=self._write("receiver_user", "receiver@example.com"),
        )

        secrets = get_test_secrets(cons)

        self.assertEqual(
            secrets,
            {
                "TAVILY_API_KEY": "tav-key",
                "SENDER_EMAIL": "sender@example.com",
                "SENDER_PASSWORD": "pwd",
                "RECEIVER_EMAIL": "receiver@example.com",
            },
        )

    def test_get_test_secrets_returns_none_when_files_missing(self):
        cons = SimpleNamespace(
            tavily_api_fpath=os.path.join(self.tmp.name, "does_not_exist_1"),
            sender_email_username_fpath=os.path.join(self.tmp.name, "does_not_exist_2"),
            sender_email_password_fpath=os.path.join(self.tmp.name, "does_not_exist_3"),
            receiver_email_username_fpath=os.path.join(self.tmp.name, "does_not_exist_4"),
        )

        secrets = get_test_secrets(cons)

        self.assertEqual(
            secrets,
            {
                "TAVILY_API_KEY": None,
                "SENDER_EMAIL": None,
                "SENDER_PASSWORD": None,
                "RECEIVER_EMAIL": None,
            },
        )

    def test_get_test_secrets_partial_files(self):
        cons = SimpleNamespace(
            tavily_api_fpath=self._write("tavily", "tav-key"),
            sender_email_username_fpath=os.path.join(self.tmp.name, "missing_sender_user"),
            sender_email_password_fpath=self._write("sender_pw", "pwd"),
            receiver_email_username_fpath=os.path.join(self.tmp.name, "missing_receiver_user"),
        )

        secrets = get_test_secrets(cons)

        self.assertEqual(secrets["TAVILY_API_KEY"], "tav-key")
        self.assertIsNone(secrets["SENDER_EMAIL"])
        self.assertEqual(secrets["SENDER_PASSWORD"], "pwd")
        self.assertIsNone(secrets["RECEIVER_EMAIL"])


if __name__ == "__main__":
    unittest.main()

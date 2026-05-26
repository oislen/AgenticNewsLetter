import os
import sys
import unittest
from unittest.mock import patch, MagicMock

NEWSLETTER_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if NEWSLETTER_DIR not in sys.path:
    sys.path.insert(0, NEWSLETTER_DIR)

import boto3 as boto3_module
from utils.boto3_session import boto3_session


class TestBoto3Session(unittest.TestCase):

    @patch.dict(
        os.environ,
        {
            "AWS_ACCESS_KEY_ID": "AKIA-TEST",
            "AWS_SECRET_ACCESS_KEY": "secret-test",
            "AWS_SESSION_TOKEN": "token-test",
        },
        clear=False,
    )
    @patch("utils.boto3_session.boto3.Session")
    def test_boto3_session_uses_env_credentials_when_set(self, mock_session_cls):
        mock_instance = MagicMock()
        mock_session_cls.return_value = mock_instance

        result = boto3_session()

        mock_session_cls.assert_called_once_with(
            aws_access_key_id="AKIA-TEST",
            aws_secret_access_key="secret-test",
            aws_session_token="token-test",
        )
        self.assertIs(result, mock_instance)

    def test_boto3_session_falls_back_to_boto3_module(self):
        env_without_creds = {
            k: v
            for k, v in os.environ.items()
            if k
            not in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN")
        }
        with patch.dict(os.environ, env_without_creds, clear=True):
            result = boto3_session()
            self.assertIs(result, boto3_module)


if __name__ == "__main__":
    unittest.main()

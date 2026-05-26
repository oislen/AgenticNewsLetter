import os
import sys
import unittest
from unittest.mock import patch, MagicMock

NEWSLETTER_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if NEWSLETTER_DIR not in sys.path:
    sys.path.insert(0, NEWSLETTER_DIR)

from nodes.publisher import publisher_node


class TestPublisherNode(unittest.TestCase):

    def setUp(self):
        self.state = {
            "topic": "Data Science",
            "subtopic": "Anomaly Detection",
            "style": "ELI5",
            "research_data": "",
            "newsletter_draft": "# Headline\n\nSome **markdown** content.",
            "steps_taken": [],
        }
        self.config = {
            "configurable": {
                "SENDER_EMAIL": "sender@example.com",
                "SENDER_PASSWORD": "secret",
                "RECEIVER_EMAIL": "receiver@example.com",
            }
        }

    @patch("nodes.publisher.smtplib.SMTP")
    def test_publisher_node_sends_email_and_returns_steps(self, mock_smtp):
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        result = publisher_node(self.state, self.config)

        mock_smtp.assert_called_once_with("smtp.gmail.com", 587)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with("sender@example.com", "secret")
        mock_server.send_message.assert_called_once()

        sent_msg = mock_server.send_message.call_args[0][0]
        self.assertEqual(sent_msg["From"], "sender@example.com")
        self.assertEqual(sent_msg["To"], "receiver@example.com")
        self.assertIn("Data Science", sent_msg["Subject"])
        self.assertIn("Anomaly Detection", sent_msg["Subject"])

        self.assertEqual(result, {"steps_taken": ["publisher_complete"]})

    @patch("nodes.publisher.smtplib.SMTP")
    def test_publisher_node_converts_markdown_to_html(self, mock_smtp):
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        publisher_node(self.state, self.config)

        sent_msg = mock_server.send_message.call_args[0][0]
        payload = sent_msg.get_payload()[0].get_payload(decode=True).decode("utf-8")
        self.assertIn("<html>", payload)
        self.assertIn("<h1>Headline</h1>", payload)
        self.assertIn("<strong>markdown</strong>", payload)

    @patch("nodes.publisher.smtplib.SMTP")
    def test_publisher_node_missing_configurable_defaults_to_none(self, mock_smtp):
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        result = publisher_node(self.state, {})

        mock_server.login.assert_called_once_with(None, None)
        self.assertEqual(result, {"steps_taken": ["publisher_complete"]})


if __name__ == "__main__":
    unittest.main()

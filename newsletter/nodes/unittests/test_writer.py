import os
import sys
import unittest
from unittest.mock import patch, MagicMock

sys.path.append(os.path.join(os.getcwd(), "newsletter"))

NEWSLETTER_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if NEWSLETTER_DIR not in sys.path:
    sys.path.insert(0, NEWSLETTER_DIR)

from nodes.writer import writer_node


class TestWriterNode(unittest.TestCase):

    def setUp(self):
        self.state = {
            "topic": "Cybersecurity",
            "subtopic": "Cryptography",
            "style": "ELI5",
            "research_data": "Some scraped technical data",
            "newsletter_draft": "",
            "steps_taken": [],
            "bedrock_client": MagicMock(),
            "bedrock_model_id": "anthropic.claude-3-haiku-20240307-v1:0",
        }
        self.config = {"configurable": {}}

    @patch("nodes.writer.ChatBedrock")
    def test_writer_node_returns_newsletter_draft(self, mock_bedrock):
        mock_llm = MagicMock()
        mock_bedrock.return_value = mock_llm
        mock_response = MagicMock()
        mock_response.content = "# Newsletter Headline\nThis is a draft."
        mock_llm.invoke.return_value = mock_response

        result = writer_node(self.state, self.config)

        self.assertIn("# Newsletter Headline", result["newsletter_draft"])
        self.assertNotIn("steps_taken", result)
        mock_llm.invoke.assert_called_once()

    @patch("nodes.writer.ChatBedrock")
    def test_writer_node_passes_bedrock_params(self, mock_bedrock):
        mock_llm = MagicMock()
        mock_bedrock.return_value = mock_llm
        mock_response = MagicMock()
        mock_response.content = "draft"
        mock_llm.invoke.return_value = mock_response

        writer_node(self.state, self.config)

        kwargs = mock_bedrock.call_args.kwargs
        self.assertIs(kwargs["client"], self.state["bedrock_client"])
        self.assertEqual(kwargs["model_id"], self.state["bedrock_model_id"])
        self.assertEqual(kwargs["model_kwargs"]["temperature"], 0.7)
        self.assertEqual(kwargs["model_kwargs"]["max_tokens"], 2048)

    @patch("nodes.writer.ChatBedrock")
    def test_writer_node_guardrail_block(self, mock_bedrock):
        mock_llm = MagicMock()
        mock_bedrock.return_value = mock_llm
        mock_llm.invoke.side_effect = Exception("Guardrail blocked this content")

        result = writer_node(self.state, self.config)

        self.assertIn("Content blocked", result["newsletter_draft"])
        self.assertIn("blocked", result["steps_taken"])

    @patch("nodes.writer.ChatBedrock")
    def test_writer_node_default_style_when_missing(self, mock_bedrock):
        mock_llm = MagicMock()
        mock_bedrock.return_value = mock_llm
        mock_response = MagicMock()
        mock_response.content = "draft"
        mock_llm.invoke.return_value = mock_response

        state = dict(self.state)
        state.pop("style")

        result = writer_node(state, self.config)

        self.assertEqual(result["newsletter_draft"], "draft")
        mock_llm.invoke.assert_called_once()


if __name__ == "__main__":
    unittest.main()

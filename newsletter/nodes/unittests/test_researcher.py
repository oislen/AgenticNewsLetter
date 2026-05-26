import os
import sys
import unittest
from unittest.mock import patch, MagicMock

sys.path.append(os.path.join(os.getcwd(), "newsletter"))

NEWSLETTER_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if NEWSLETTER_DIR not in sys.path:
    sys.path.insert(0, NEWSLETTER_DIR)

from nodes.researcher import researcher_node


class TestResearcherNode(unittest.TestCase):

    def setUp(self):
        self.state = {
            "topic": "Quantum Computing",
            "subtopic": "Error Correction",
            "style": "ELI5",
            "research_data": "",
            "newsletter_draft": "",
            "steps_taken": [],
        }
        self.config = {"configurable": {"TAVILY_API_KEY": "tavily-key-xyz"}}

    @patch("nodes.researcher.TavilySearchAPIWrapper")
    @patch("nodes.researcher.TavilySearch")
    def test_researcher_node_formats_results(self, mock_tavily, mock_wrapper):
        mock_search = MagicMock()
        mock_tavily.return_value = mock_search
        mock_search.invoke.return_value = {
            "results": [
                {
                    "title": "Test News",
                    "url": "http://test.com",
                    "content": "Useful info",
                },
                {
                    "title": "Another Story",
                    "url": "http://example.com",
                    "content": "More info",
                },
            ]
        }

        result = researcher_node(self.state, self.config)

        self.assertIn("Test News", result["research_data"])
        self.assertIn("http://test.com", result["research_data"])
        self.assertIn("Useful info", result["research_data"])
        self.assertIn("Another Story", result["research_data"])
        self.assertIn("---", result["research_data"])
        self.assertEqual(result["steps_taken"], ["researcher_complete"])
        mock_search.invoke.assert_called_once()

    @patch("nodes.researcher.TavilySearchAPIWrapper")
    @patch("nodes.researcher.TavilySearch")
    def test_researcher_node_builds_query_with_topic_and_subtopic(
        self, mock_tavily, mock_wrapper
    ):
        mock_search = MagicMock()
        mock_tavily.return_value = mock_search
        mock_search.invoke.return_value = {"results": []}

        researcher_node(self.state, self.config)

        invoke_args = mock_search.invoke.call_args[0][0]
        self.assertIn("Quantum Computing", invoke_args["query"])
        self.assertIn("Error Correction", invoke_args["query"])

    @patch("nodes.researcher.TavilySearchAPIWrapper")
    @patch("nodes.researcher.TavilySearch")
    def test_researcher_node_passes_api_key_to_wrapper(self, mock_tavily, mock_wrapper):
        mock_search = MagicMock()
        mock_tavily.return_value = mock_search
        mock_search.invoke.return_value = {"results": []}

        researcher_node(self.state, self.config)

        mock_wrapper.assert_called_once_with(tavily_api_key="tavily-key-xyz")

    @patch("nodes.researcher.TavilySearchAPIWrapper")
    @patch("nodes.researcher.TavilySearch")
    def test_researcher_node_empty_results(self, mock_tavily, mock_wrapper):
        mock_search = MagicMock()
        mock_tavily.return_value = mock_search
        mock_search.invoke.return_value = {"results": []}

        result = researcher_node(self.state, self.config)

        self.assertEqual(result["research_data"], "")
        self.assertEqual(result["steps_taken"], ["researcher_complete"])


if __name__ == "__main__":
    unittest.main()

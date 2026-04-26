import pytest
from unittest.mock import MagicMock, patch
from nodes.researcher import researcher_node
from nodes.writer import writer_node

@pytest.fixture
def mock_state():
    return {
        "topic": "Quantum Computing",
        "style": "ELI5",
        "research_data": "",
        "newsletter_draft": "",
        "steps_taken": []
    }

# --- Test the Researcher Node ---
@patch("src.nodes.researcher.TavilySearch")
def test_researcher_node_success(mock_tavily, mock_state):
    # Setup mock return value
    mock_inst = mock_tavily.return_value
    mock_inst.invoke.return_value = [
        {"title": "Test News", "url": "http://test.com", "content": "Useful info"}
    ]

    result = researcher_node(mock_state)

    assert "Test News" in result["research_data"]
    assert "researcher_complete" in result["steps_taken"]
    mock_inst.invoke.assert_called_once()

# --- Test the Writer Node (AWS Bedrock Mock) ---
@patch("src.nodes.writer.ChatBedrock")
def test_writer_node_logic(mock_bedrock, mock_state):
    # Simulate research data already being present
    mock_state["research_data"] = "Some scraped technical data"
    
    # Mock the LLM response
    mock_llm = mock_bedrock.return_value
    mock_response = MagicMock()
    mock_response.content = "# Newsletter Headline\nThis is a draft."
    mock_llm.invoke.return_value = mock_response

    result = writer_node(mock_state)

    assert "# Newsletter Headline" in result["newsletter_draft"]
    assert len(result["newsletter_draft"]) > 0
    mock_llm.invoke.assert_called_once()

# --- Test Guardrail Failure Simulation ---
@patch("src.nodes.writer.ChatBedrock")
def test_writer_node_guardrail_block(mock_bedrock, mock_state):
    mock_llm = mock_bedrock.return_value
    # Simulate an AWS exception (like a Guardrail Block)
    mock_llm.invoke.side_effect = Exception("Guardrail blocked this content")

    result = writer_node(mock_state)

    assert "Content blocked" in result["newsletter_draft"]
    assert "blocked" in result["steps_taken"]
from langchain_core.language_models.fake import FakeListLLM
from graph import builder

def test_full_graph_structure():
    # Compile the graph
    graph = builder.compile()
    
    # Check if all nodes are present
    assert "researcher" in graph.nodes
    assert "writer" in graph.nodes
    assert "publisher" in graph.nodes
import os
import sys
import unittest

sys.path.append(os.path.join(os.getcwd(), "newsletter"))

NEWSLETTER_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if NEWSLETTER_DIR not in sys.path:
    sys.path.insert(0, NEWSLETTER_DIR)


class TestFullGraphStructure(unittest.TestCase):

    def test_graph_contains_all_expected_nodes(self):
        from graph import builder

        graph = builder.compile()
        self.assertIn("researcher", graph.nodes)
        self.assertIn("writer", graph.nodes)
        self.assertIn("publisher", graph.nodes)


if __name__ == "__main__":
    unittest.main()

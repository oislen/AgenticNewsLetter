import os
import sys
import unittest

sys.path.append(os.path.join(os.getcwd(), "newsletter"))

NEWSLETTER_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if NEWSLETTER_DIR not in sys.path:
    sys.path.insert(0, NEWSLETTER_DIR)


class TestNodesPackage(unittest.TestCase):

    def test_node_callables_are_exposed(self):
        from nodes import publisher_node, researcher_node, writer_node

        self.assertTrue(callable(publisher_node))
        self.assertTrue(callable(researcher_node))
        self.assertTrue(callable(writer_node))


if __name__ == "__main__":
    unittest.main()

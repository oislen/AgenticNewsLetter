import os
import sys
import unittest

NEWSLETTER_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if NEWSLETTER_DIR not in sys.path:
    sys.path.insert(0, NEWSLETTER_DIR)

from utils.topics import topics


class TestTopics(unittest.TestCase):

    def test_topics_is_dict(self):
        self.assertIsInstance(topics, dict)

    def test_topics_contains_expected_categories(self):
        expected_categories = {
            "Data Science / Machine Learning / AI",
            "Software Development / Programming",
            "Cybersecurity / Application Security",
            "Start Ups / Entrepreneurship",
            "Investments / Personal Finance",
        }
        self.assertTrue(expected_categories.issubset(set(topics.keys())))

    def test_each_topic_maps_to_non_empty_list_of_strings(self):
        for category, subtopics in topics.items():
            self.assertIsInstance(subtopics, list, f"{category} is not a list")
            self.assertGreater(len(subtopics), 0, f"{category} has no subtopics")
            for subtopic in subtopics:
                self.assertIsInstance(subtopic, str)
                self.assertGreater(len(subtopic), 0)


if __name__ == "__main__":
    unittest.main()

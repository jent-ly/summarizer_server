import unittest
import summarizer_server.tests.test_utils as utils
from summarizer_server.text_rank import TextRank


class TestTextRank(unittest.TestCase):
    def setUp(self):
        self.text_rank = TextRank()

    def test_article1_returns_15_percent_of_sentences(self):
        article = utils.get_article1_contents()
        all_top_sentences = self.text_rank.summarize(article, 100)
        top_15p_sentences = self.text_rank.summarize(article, 15)
        self.assertEqual(len(all_top_sentences) * 15 // 100, len(top_15p_sentences))


if __name__ == "__main__":
    unittest.main()

import unittest
import summarizer_server.tests.test_utils as utils
import math
import pdb

from nltk import tokenize
from summarizer_server.text_rank import TextRank


class TestTextRank(unittest.TestCase):
    def setUp(self):
        self.text_rank = TextRank()

    def test_process_html(self):
        article_html = utils.get_article_contents("article1.html")
        expected_article_text = utils.get_article_contents("article1.txt")
        article = self.text_rank.process_html(article_html)

        self.assertEqual(
            "Poll finds Raptors’ playoff run has attracted new fans across Canada",
            article.title,
        )
        self.assertEqual(expected_article_text, article.text)
        self.assertEqual("en", article.config.get_language())

    def test_summarize_from_html(self):
        article_html = utils.get_article_contents("article2.html")

        summary = self.text_rank.summarize_from_html(article_html, 15)
        self.assertTrue(summary)

    def test_evaluate_newspaper_summary_deterministic(self):
        article = utils.get_article_contents("article2.txt")
        sentences = tokenize.sent_tokenize(article)

        scores = self.text_rank.evaluate_newspaper_summary(
            "What's inside the Barcode?", article, sentences, "en"
        )

        ranked_sentences = sorted(((v, k[1]) for k, v in scores.items()), reverse=True)
        top_sentences = list(
            score_sentence_tuple[1] for score_sentence_tuple in ranked_sentences[:3]
        )
        self.assertListEqual(
            [
                "If the Scanner doesn’t find it, it will not acknowledge the EAN13 barcode.",
                "In this article, we’re gonna take an example of the EAN13 barcode.",
                "What’s inside the Barcode?",
            ],
            top_sentences,
        )

    def test_evaluate_newspaper_summary_returns_normalized_scores(self):
        article = utils.get_article_contents("article2.txt")
        sentences = tokenize.sent_tokenize(article)

        scores = self.text_rank.evaluate_newspaper_summary(
            "What's inside the Barcode?", article, sentences, "en"
        )

        score_sum = sum(scores.values())
        self.assertEqual(1, score_sum)

    def test_evaluate_textrank_summary_returns_normalized_scores(self):
        # evaluate_textrank_summary depends heavily on word vectorizations
        # which are impractical to load on every test run, so this is all we can do
        article = utils.get_article_contents("article1.txt")
        sentences = tokenize.sent_tokenize(article)

        scores = self.text_rank.evaluate_textrank_summary(sentences)

        score_sum = sum(scores.values())
        self.assertEqual(1, score_sum)

    def test_summarize_returns_15_percent_of_sentences(self):
        article = utils.get_article_contents("article1.txt")
        sentences = tokenize.sent_tokenize(article)

        all_top_sentences = self.text_rank.summarize("test title", article, "en", 100)
        top_15p_sentences = self.text_rank.summarize("test title", article, "en", 15)

        self.assertEqual(len(sentences), len(all_top_sentences))
        self.assertEqual(
            math.ceil(len(all_top_sentences) * 15 / 100), len(top_15p_sentences)
        )

    def test_summarize_one_sentence(self):
        summary = self.text_rank.summarize("Hello world!", "Hello world!", "en", 100)

        self.assertListEqual([], summary)

    def test_summarize_default_language(self):
        summary = self.text_rank.summarize(
            "Hello world!", "Hello world! Welcome.", None, 100
        )

        self.assertListEqual(["Welcome."], summary)


if __name__ == "__main__":
    unittest.main()

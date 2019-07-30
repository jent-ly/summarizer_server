import logging
import pickle
import os
import re

import networkx as nx
import nltk
import numpy as np
import pandas as pd

from collections import Counter
from nltk import tokenize
from nltk import corpus
from sklearn.metrics.pairwise import cosine_similarity
from newspaper import Article
from newspaper import nlp
from image_setup import WORD_EMBEDDINGS_FILE

log = logging.getLogger("summarizer_server")


class TextRank:
    def __init__(self):
        self.word_embeddings = {}
        self.stop_words = set()

    def setup(self):
        # TODO: consider how to handle languages other than English
        self.stop_words = set(corpus.stopwords.words("english"))
        with open(WORD_EMBEDDINGS_FILE, "rb") as handle:
            self.word_embeddings = pickle.load(handle)

    def _remove_stopwords(self, sen):
        sen_new = " ".join([i for i in sen if i not in self.stop_words])
        return sen_new

    def process_html(self, html):
        # fetch page content and parse html using newspaper
        article = Article(url="")
        article.set_html(html)
        article.parse()

        return article

    def normalize_scores(self, scores):
        total = sum(scores.values())
        return {key: score / total for key, score in scores.items()}

    # Implemented following:
    #     https://www.analyticsvidhya.com/blog/2018/11/introduction-text-summarization-textrank-python/
    def summarize(self, html, percent_sentences):
        if (
            percent_sentences is None
            or percent_sentences > 100
            or percent_sentences < 0
        ):
            percent_sentences = 15

        article = self.process_html(html)

        # remove title from the text, if it appears in the text
        if article.text.startswith(article.title):
            article.set_text(article.text[len(article.title) :])

        sentences = nlp.split_sentences(article.text)
        log.debug(article.text)

        # remove punctuations, numbers and special characters
        clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")
        clean_sentences = [s.lower() for s in clean_sentences]
        clean_sentences = [self._remove_stopwords(r.split()) for r in clean_sentences]

        # create sentence vectors
        sentence_vectors = []
        for i in clean_sentences:
            if len(i) != 0:
                v = sum(
                    [self.word_embeddings.get(w, np.zeros((300,))) for w in i.split()]
                ) / (len(i.split()) + 0.001)
            else:
                v = np.zeros((300,))
            sentence_vectors.append(v)

        # similarity matrix
        sim_mat = np.zeros([len(sentences), len(sentences)])

        # initialize matrix
        for i in range(len(sentences)):
            for j in range(len(sentences)):
                if i != j:
                    sim_mat[i][j] = cosine_similarity(
                        sentence_vectors[i].reshape(1, 300),
                        sentence_vectors[j].reshape(1, 300),
                    )[0, 0]

        # convert matrix into graph
        nx_graph = nx.from_numpy_array(sim_mat)
        textrank_scores = self.normalize_scores(nx.pagerank(nx_graph))

        # get newspaper's nlp scores
        # https://github.com/codelucas/newspaper/blob/master/newspaper/article.py#L372
        nlp.load_stopwords(article.config.get_language())

        # call to: nlp.summarize(title=article.title, text=article.text, max_sents=max_sents)
        # https://github.com/codelucas/newspaper/blob/master/newspaper/nlp.py#L40
        title_words = nlp.split_words(article.title)
        most_frequent = nlp.keywords(article.text)

        nlp_scores = self.normalize_scores(
            nlp.score(sentences, title_words, most_frequent)
        )

        totalled_scores = Counter()
        for key, value in nlp_scores.items():
            totalled_scores[key[0]] += value

        for key, value in textrank_scores.items():
            totalled_scores[key] += value

        num_sentences = int(len(clean_sentences) * percent_sentences / 100)
        sentence_indices = list(
            map(lambda x: x[0], totalled_scores.most_common(num_sentences))
        )

        return list(map(lambda x: sentences[x], sentence_indices))

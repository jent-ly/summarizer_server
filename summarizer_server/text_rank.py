import logging
import pickle
import math
import os
import re
import pdb

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
    def evaluate_textrank_summary(self, sentences):
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

        # return a dictionary of index to sentences and their scores
        # ie. { 0: 0.145, 1: 0.105, 2: 0.127, 3: 0.123, 4: 0.120, 5: 0.154, 6: 0.101, 7: 0.125 }
        return textrank_scores

    def evaluate_newspaper_summary(self, title, text, sentences, language):
        # get newspaper's nlp scores
        # https://github.com/codelucas/newspaper/blob/master/newspaper/article.py#L372
        nlp.load_stopwords(language)

        # call to: nlp.summarize(title=article.title, text=article.text, max_sents=max_sents)
        # https://github.com/codelucas/newspaper/blob/master/newspaper/nlp.py#L40
        title_words = nlp.split_words(title)
        most_frequent = nlp.keywords(text)

        nlp_scores = self.normalize_scores(
            nlp.score(sentences, title_words, most_frequent)
        )

        # Return a dictionary of tuple<sentence index, setence text> to score
        # ie. { (0, 'A new poll suggests that the Toronto Raptors...') : 0.144, ... }
        return nlp_scores

    def summarize_from_html(self, html, percent_sentences):
        # Use newspaper3k's clean text extraction and parsing
        article = self.process_html(html)
        return self.summarize(
            article.title,
            article.text,
            article.config.get_language(),
            percent_sentences,
        )

    def summarize(self, title, text, language, percent_sentences):
        # remove title from the text, if it appears in the text
        if text.startswith(title):
            text = text[len(title) :]

        if not text:
            return []

        if not language:
            language = "en"

        text = text.lstrip()
        sentences = tokenize.sent_tokenize(text)

        textrank_scores = self.evaluate_textrank_summary(sentences)
        newspaper_scores = self.evaluate_newspaper_summary(
            title, text, sentences, language
        )

        totalled_scores = Counter()
        for key, value in newspaper_scores.items():
            totalled_scores[key[0]] += value

        for key, value in textrank_scores.items():
            totalled_scores[key] += value

        num_sentences = int(math.ceil(len(sentences) * percent_sentences / 100))
        sentence_indices = list(
            map(lambda x: x[0], totalled_scores.most_common(num_sentences))
        )

        return list(map(lambda x: sentences[x], sentence_indices))

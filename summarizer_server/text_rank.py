import pickle
import os
import re

import networkx as nx
import nltk
import numpy as np
import pandas as pd
from nltk import tokenize
from nltk import corpus
from sklearn.metrics.pairwise import cosine_similarity
from image_setup import WORD_EMBEDDINGS_FILE


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

    # Implemented following:
    #     https://www.analyticsvidhya.com/blog/2018/11/introduction-text-summarization-textrank-python/
    def summarize(self, input_text, percent_sentences):
        if percent_sentences is None or percent_sentences > 100 or precent_senteces < 0:
            percent_sentences = 15

        sentences = tokenize.sent_tokenize(input_text)

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
        scores = nx.pagerank(nx_graph)

        ranked_sentences = sorted(
            ((scores[i], i) for i in range(len(sentences))), reverse=True
        )

        # Extract top 15% of sentences
        top_sentences = []
        for i in range(int(len(clean_sentences) * percent_sentences / 100)):
            top_sentences.append(sentences[ranked_sentences[i][1]])

        return top_sentences

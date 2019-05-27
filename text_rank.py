import numpy as np
import pandas as pd
import nltk
from nltk import tokenize
from nltk import corpus
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import re

word_embeddings = {}
stop_words = []


def setup():
    nltk.download("punkt")
    nltk.download("stopwords")

    # TODO: consider how to handle languages other than English
    stop_words = corpus.stopwords.words("english")

    f = open("/data/glove.6B.100d.txt", encoding="utf-8")
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype="float32")
        word_embeddings[word] = coefs
    f.close()


def remove_stopwords(sen):
    sen_new = " ".join([i for i in sen if i not in stop_words])
    return sen_new


# Implemented following:
#     https://www.analyticsvidhya.com/blog/2018/11/introduction-text-summarization-textrank-python/
def summarize(input_text):
    sentences = tokenize.sent_tokenize(input_text)

    # remove punctuations, numbers and special characters
    clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")
    clean_sentences = [s.lower() for s in clean_sentences]
    clean_sentences = [remove_stopwords(r.split()) for r in clean_sentences]

    # create sentence vectors
    sentence_vectors = []
    for i in clean_sentences:
        if len(i) != 0:
            v = sum([word_embeddings.get(w, np.zeros((100,))) for w in i.split()]) / (
                len(i.split()) + 0.001
            )
        else:
            v = np.zeros((100,))
        sentence_vectors.append(v)

    # similarity matrix
    sim_mat = np.zeros([len(sentences), len(sentences)])

    # initialize matrix
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j:
                sim_mat[i][j] = cosine_similarity(
                    sentence_vectors[i].reshape(1, 100),
                    sentence_vectors[j].reshape(1, 100),
                )[0, 0]

    # convert matrix into graph
    nx_graph = nx.from_numpy_array(sim_mat)
    scores = nx.pagerank(nx_graph)

    ranked_sentences = sorted(
        ((scores[i], s) for i, s in enumerate(sentences)), reverse=True
    )

    # Extract top 5 sentences as the summary
    top_sentences = []
    for i in range(5):
        top_sentences.append(re.sub(r"[^\x00-\x7f]", r"", ranked_sentences[i][1]))

    return top_sentences

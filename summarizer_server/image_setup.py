import pickle
import os

import nltk
import numpy as np

WORD_EMBEDDINGS_FILE = "/data/word_embeddings.pickle"

REQUIRED_CORPORA = [
    "brown",  # Required for FastNPExtractor
    "punkt",  # Required for WordTokenizer
    "maxent_treebank_pos_tagger",  # Required for NLTKTagger
    "movie_reviews",  # Required for NaiveBayesAnalyzer
    "wordnet",  # Required for lemmatization and Wordnet
    "stopwords",
]

# This should be run from the Dockerfile
def setup_local_data():
    for corpus in REQUIRED_CORPORA:
        print(('Downloading "{0}"'.format(corpus)))
        nltk.download(corpus)

    if (
        os.path.exists(WORD_EMBEDDINGS_FILE)
        and os.path.getsize(WORD_EMBEDDINGS_FILE) > 0
    ):
        return

    word_embeddings = {}
    with open("/data/glove.6B.300d.txt", "r", encoding="utf-8") as file:
        for line in file:
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:], dtype="float32")
            word_embeddings[word] = coefs

    with open(WORD_EMBEDDINGS_FILE, "wb") as handle:
        pickle.dump(word_embeddings, handle)

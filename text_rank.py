import numpy as np
import pandas as pd
import nltk
from nltk import tokenize
import re

nltk.download('punkt')

# Implemented following: 
#     https://www.analyticsvidhya.com/blog/2018/11/introduction-text-summarization-textrank-python/
def summarize(input_text):
    sentences = tokenize.sent_tokenize(input_text);
    print(sentences)


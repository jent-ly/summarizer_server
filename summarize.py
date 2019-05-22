# -*- coding: utf-8 -*-

# A file that reads the sample text and passes it to the summarizer
import text_rank
import sys
import io

print("Starting text rank summarizer...")

files = ["sample_text1.txt"]

for file_name in files:
    print("Reading file: " + file_name)
    f = io.open(file_name, "rU", encoding="utf-8")
    input_text = f.read()
    f.close()
    text_rank.summarize(input_text)

    


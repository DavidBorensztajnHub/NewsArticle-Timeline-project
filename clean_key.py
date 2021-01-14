# libraries
import pandas as pd, numpy as np
from pathlib import Path
import ast
from sklearn.feature_extraction.text import CountVectorizer
import re
from nltk.corpus import stopwords

# load data
parent_path = Path.cwd().parent
df = pd.read_csv("../dataframe2.csv", converters=
{"header":ast.literal_eval,"intro":ast.literal_eval})

stop_words = set(stopwords.words("english"))##Creating a list of custom stopwords
new_words = ["using", "show", "result", "large", "also", "iv", "one", "two", "new", "previously", "shown", "mr"]
stop_words = stop_words.union(new_words)

#Most frequently occuring words
def get_top_n_words(corpus, n=20):
    corpus = [corpus]
    if len(str(corpus).split(" "))==1:
        return 0
    vec = CountVectorizer(stop_words=stop_words, max_features=10000, ngram_range=(1,3)).fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in      
                vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], 
                    reverse=True)
    return words_freq[:n]

    #Convert most freq words to dataframe for plotting bar plot
df["top_n_words"] = df["text"].apply(get_top_n_words)

df.to_csv(parent_path/ "dataframe2_key.csv", index=False)
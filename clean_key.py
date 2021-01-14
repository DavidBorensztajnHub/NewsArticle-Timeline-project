# libraries
import pandas as pd, numpy as np
from pathlib import Path
import ast
from sklearn.feature_extraction.text import CountVectorizer
import re
from nltk.corpus import stopwords
from collections import Counter

# load data
df = pd.read_json("../dataframe.json").head(100)

# creating a list of custom stopwords
stop_words = set(stopwords.words("english"))
new_words = ["using", "show", "result", "large", "also", "iv", "one",
 "two", "new", "previously", "shown", "mr"]
stop_words = stop_words.union(new_words)

# most frequently occuring words
def get_top_n_words(corpus, n=20):
    if corpus == ["empty"]:
        return corpus
    vec = CountVectorizer(stop_words=stop_words, max_features=10000, ngram_range=(1,3)).fit(corpus)
    bag_of_words = vec.transform(corpus)
    print(bag_of_words.shape)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in      
                vec.vocabulary_.items()]
    words_freq = sorted(words_freq, key = lambda x: x[1], 
                    reverse=True)
    return words_freq[:n]

def get_top_n_words2(corpus, n=20):
    if corpus == ["empty"]:
        return corpus
    return [(w,c) for w,c in Counter(corpus).most_common(n) if w not in new_words]

# convert most freq words to dataframe for plotting bar plot
df["top_n_words"] = [get_top_n_words2(x) for x in df["text"]]

df.to_csv("../dataframe_key.csv", index=False)
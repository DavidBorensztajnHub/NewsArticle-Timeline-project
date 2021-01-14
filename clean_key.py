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

stop_words = set(stopwords.words("english"))

# Creating a list of custom stopwords
new_words = ["using", "show", "result", "large", "also", "iv", "one", "two", "new", "previously", "shown", "mr"]
stop_words = stop_words.union(new_words)

# Most frequently occuring words
def get_top_n_words(corpus, n, stop_words, ngram_range):
    corpus = [corpus]
    if len(str(corpus).split(" "))==1:
        return [(0,0)]
    vec = CountVectorizer(stop_words=stop_words, max_features=10000, ngram_range=ngram_range).fit(corpus)
    bag_of_words = vec.transform(corpus) 
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in      
                vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], 
                    reverse=True)
    return words_freq[:n]

# function the frequency from the words
def split_freq(df):
    top_n_words = []
    for words, freq in df:
        top_n_words.append(words)
    return top_n_words

# applying functions to dataframe
df["top_n_words"] = df['text'].apply(get_top_n_words, args=(20, stop_words, (1,3)))
df["top_n_words_2"] = df['text'].apply(get_top_n_words, args=(20, stop_words, (2,3)))
df["top_n_words_3"] = df['text'].apply(get_top_n_words, args=(20, stop_words, (3,3)))

df['top_words'] = df['top_n_words'].apply(split_freq)
df['top_words_2'] = df['top_n_words_2'].apply(split_freq)
df['top_words_3'] = df['top_n_words_3'].apply(split_freq)

print(df['top_words_3'].head())

# safe dataframe in csv file
df.to_csv(parent_path/ "dataframe2_key.csv", index=False)
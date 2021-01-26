"""
takes as input either the filtered dataset
or the wikipedia text files and finds
the most common word combinations
(of 1, 2 and 3 words)
"""

# libraries
import pandas as pd, numpy as np
from pathlib import Path
import ast
from sklearn.feature_extraction.text import CountVectorizer
import re
from nltk.corpus import stopwords
from collections import Counter
from wikipedia_processing import remove_wikipedia_crap

# load data
parent_path = Path.cwd().parent
data = pd.read_json("../wiki_df.json")

# creating a list of custom stopwords
stop_words = set(stopwords.words("english"))
new_words = ["using", "show", "result", "large", "also", "iv", "one",
 "two", "new", "previously", "shown", "mr"]
stop_words = stop_words.union(new_words)

# most frequently occuring words
def get_top_n_words(corpus, n, stop_words, ngram_range):
    if corpus == ["empty"]:
        return corpus
    vec = CountVectorizer(stop_words=stop_words, max_features=10000, ngram_range=ngram_range).fit(corpus)
    bag_of_words = vec.transform(corpus) 
    words_freq = list(vec.vocabulary_.keys())
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in      
                vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], 
                    reverse=True)
    return words_freq[:n]

"""
brams versie van top words, werkt alleen met ngram (1,3) maar is wel sneller
def get_top_n_words2(corpus, n=20):
    if corpus == ["empty"]:
        return corpus
    return [(w,c) for w,c in Counter(corpus).most_common(n) if w not in new_words]
"""

# find most occuring words in article text
#df["top_n_words"] = [get_top_n_words2(x) for x in df["text"]]

# create df
topics = ["covid","blm","bxt","f1", "impeach"]
wiki_df = pd.DataFrame(data={"all_words":" "},index=topics)

# add wikipedia words to df
file_contents = []
for topic in topics:
    file = open(f"../wiki_{topic}.txt","r")
    content = file.readlines()
    content = remove_wikipedia_crap(content[0])
    file_contents.append(content)

# find most occuring n grams and put in df
wiki_df["all_words"] = file_contents
n = 5
for i in range(1,4):
    wiki_df[f"top_{str(i)}"] = [get_top_n_words(x, n, stop_words, (i,3)) for x in wiki_df["all_words"]]
    wiki_df[f"top_{str(i)}"] = [[word for word,freq in tuple] for tuple in wiki_df[f"top_{str(i)}"]]

# save dataframe as json file
wiki_df.to_json(parent_path / "wiki_df.json")

# save dataframe as csv file
wiki_df.to_csv(parent_path / "wiki_df.csv")
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

wiki_corona_file = open("../wiki_corona.txt", "r")
wiki_corona = wiki_corona_file.readlines()
wiki_df = pd.DataFrame(wiki_corona)
wiki_df.columns = ["corona"]
print(wiki_df)

wiki_blm_file = open("../wiki_blm.txt", "r")
wiki_blm = wiki_blm_file.readlines()
wiki_df["blm"] = wiki_blm

wiki_bxt_file = open("../wiki_bxt.txt", "r")
wiki_bxt = wiki_bxt_file.readlines()
wiki_df["bxt"] = wiki_bxt

wiki_f1_file = open("../wiki_f1.txt", "r")
wiki_f1 = wiki_f1_file.readlines()
wiki_df["f1"] = wiki_f1

stop_words = set(stopwords.words("english"))

# Creating a list of custom stopwords
new_words = ["using", "show", "result", "large", "also", "iv", "one", "two", "new", "previously", "shown", "mr", 'wikipedia', 'retrieved', 'archieved']
stop_words = stop_words.union(new_words)

# Most frequently occuring words
def get_top_n_words(corpus, n, stop_words, ngram_range):
    corpus = [corpus]
    if len(str(corpus).split(" "))==1:
        return [(0,0)]
    vec = CountVectorizer(stop_words=stop_words, max_features=10000, ngram_range=ngram_range).fit(corpus)
    bag_of_words = vec.transform(corpus) 
    words_freq = list(vec.vocabulary_.keys())
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in      
                vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], 
                    reverse=True)
    return words_freq[:n]

# function the frequency from the words
def split_freq(df):
    top_n_words = []
    for words, frq in df:
        top_n_words.append(words)
    return top_n_words

# applying functions to dataframe
#df["top_n_words"] = df['text'].apply(get_top_n_words, args=(20, stop_words, (1,3)))
#df["top_n_words_2"] = df['text'].apply(get_top_n_words, args=(20, stop_words, (2,3)))
#df["top_n_words_3"] = df['text'].apply(get_top_n_words, args=(20, stop_words, (3,3)))

#df['top_words'] = df['top_n_words'].apply(split_freq)
#df['top_words_2'] = df['top_n_words_2'].apply(split_freq)
#df['top_words_3'] = df['top_n_words_3'].apply(split_freq)


# top words wiki covid
wiki_df['corona_top_1'] = wiki_df["corona"].apply(get_top_n_words, args=(20, stop_words, (1,3)))
wiki_df['corona_top_2'] = wiki_df["corona"].apply(get_top_n_words, args=(20, stop_words, (2,3)))
wiki_df['corona_top_3'] = wiki_df["corona"].apply(get_top_n_words, args=(20, stop_words, (3,3)))

wiki_df['corona_top_1'] = wiki_df['corona_top_1'].apply(split_freq)
wiki_df['corona_top_2'] = wiki_df['corona_top_2'].apply(split_freq)
wiki_df['corona_top_3'] = wiki_df['corona_top_3'].apply(split_freq)

# top words wiki blm
wiki_df['blm_top_1'] = wiki_df["blm"].apply(get_top_n_words, args=(20, stop_words, (1,3)))
wiki_df['blm_top_2'] = wiki_df["blm"].apply(get_top_n_words, args=(20, stop_words, (2,3)))
wiki_df['blm_top_3'] = wiki_df["blm"].apply(get_top_n_words, args=(20, stop_words, (3,3)))

wiki_df['blm_top_1'] = wiki_df['blm_top_1'].apply(split_freq)
wiki_df['blm_top_2'] = wiki_df['blm_top_2'].apply(split_freq)
wiki_df['blm_top_3'] = wiki_df['blm_top_3'].apply(split_freq)

# top words wiki bxt
wiki_df['bxt_top_1'] = wiki_df["bxt"].apply(get_top_n_words, args=(20, stop_words, (1,3)))
wiki_df['bxt_top_2'] = wiki_df["bxt"].apply(get_top_n_words, args=(20, stop_words, (2,3)))
wiki_df['bxt_top_3'] = wiki_df["bxt"].apply(get_top_n_words, args=(20, stop_words, (3,3)))

wiki_df['bxt_top_1'] = wiki_df['bxt_top_1'].apply(split_freq)
wiki_df['bxt_top_2'] = wiki_df['bxt_top_2'].apply(split_freq)
wiki_df['bxt_top_3'] = wiki_df['bxt_top_3'].apply(split_freq)

# top words wiki bxt
wiki_df['f1_top_1'] = wiki_df["f1"].apply(get_top_n_words, args=(20, stop_words, (1,3)))
wiki_df['f1_top_2'] = wiki_df["f1"].apply(get_top_n_words, args=(20, stop_words, (2,3)))
wiki_df['f1_top_3'] = wiki_df["f1"].apply(get_top_n_words, args=(20, stop_words, (3,3)))

wiki_df['f1_top_1'] = wiki_df['f1_top_1'].apply(split_freq)
wiki_df['f1_top_2'] = wiki_df['f1_top_2'].apply(split_freq)
wiki_df['f1_top_3'] = wiki_df['f1_top_3'].apply(split_freq)

print(wiki_df.head())

# safe dataframe in csv file
wiki_df.to_csv(parent_path/ "wiki_df.csv", index=True)
df.to_csv(parent_path/ "dataframe2_key.csv", index=False)
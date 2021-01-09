"""
This program loads the json dataset and 
preprocesses the data by removing irrelevant
words and punctuation. it then stores the
data in a .csv file
"""

# libraries
import json, pandas as pd, numpy as np
import string, re, nltk
from bs4 import BeautifulSoup
from pathlib import Path

# load data
def open_json(filepath):
    articles = []
    file = open(filepath)
    i=0
    for article in file:
        articles.append(json.loads(article))
        i+=1
        if i > 100: break
    file.close()
    return articles

parent_path = Path.cwd().parent
articles = open_json(parent_path / "articles_en_2020_raw.json")

# get dates and bodies for each article
dates = [article["date"] for article in articles]
bodies = [article["body"] for article in articles]

# unpack body into title, intro and text
def unpack_bodies(bodies):
    intros = [next((sec["content"] for sec in body if sec["type"]=="intro"), None) for body in bodies]
    headers = [next((sec["content"] for sec in body if sec["type"]=="hl1"), None) for body in bodies]
    paragraphs = [" ".join([sec["content"] for sec in body if sec["type"] == "p"]) for body in bodies]
    return intros, headers, paragraphs

intros, headers, pars = unpack_bodies(bodies)

# put articles into pandas dataframe
df = pd.DataFrame({"date":dates, "header":headers, "intro":intros, "text": pars})

# functions for cleaning up text
# remove html punctuation
def remove_html_punct(text):
    # remove html tags
    text = BeautifulSoup(text,features="html.parser").get_text()
    
    # remove punctuation
    punc = string.punctuation  
    no_punct = [words for words in text if words not in punc]
    words_wo_punct=''.join(no_punct)
    return words_wo_punct.lower()

# split text into separate words
def tokenize(text):
    return nltk.tokenize.word_tokenize(text)

# remove meaningless common words
def remove_stopwords(text):
    stopword = nltk.corpus.stopwords.words('english')
    text = [word for word in text if word not in stopword]
    return text

# find articles that have an intro
has_intro = df["intro"].apply(lambda x: x != None)

# apply functions
df["header"] = df["header"].apply(remove_html_punct)
df["text"] = df["text"].apply(remove_html_punct)
df.loc[has_intro,"intro"] = df.loc[has_intro,"intro"].apply(remove_html_punct)

df["header"] = df["header"].apply(tokenize)
df["text"] = df["text"].apply(tokenize)
df.loc[has_intro,"intro"] = df.loc[has_intro,"intro"].apply(tokenize)

df[["intro","header","text"]] = df[["intro","header","text"]].apply(remove_stopwords)

df.to_csv(parent_path / "dataframe2.csv")
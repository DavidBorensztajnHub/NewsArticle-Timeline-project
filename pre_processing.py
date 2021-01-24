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
import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer

# load data
def open_json(filepath):
    articles = []
    file = open(filepath)
    i=0
    for article in file:
        #if i  10 == 0:
        articles.append(json.loads(article))
        i+=1
        if i > 30000: break
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

# fill empty cells with string
df = df.fillna("empty")
df = df.replace("","empty")

# find articles that have an intro
has_intro = df["intro"].apply(lambda x: x != "empty")

# functions for cleaning up text
# remove html punctuation
def remove_html_punct(text):
    # remove html tags
    if text:
        text = BeautifulSoup(text,features="html.parser").get_text()
    
        # remove punctuation
        punc = string.punctuation + "“”‘’—"
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

def lemmatizing(text):
    lemmatizer = WordNetLemmatizer()
    text = [lemmatizer.lemmatize(word) for word in text]
    return text

def stemming(text):
    ps = PorterStemmer()
    text=[ps.stem(word) for word in text]
    return text

# apply preprocessing functions
columns = ["header","intro","text"]
for col in columns:
    df[col] = [lemmatizing(remove_stopwords(tokenize(remove_html_punct(x)))) for x in df[col]]

# set first 20 words of text as intro for articles that don't have an intro
df.loc[~has_intro,"intro"] = df.loc[~has_intro,"text"[:20]]

df.to_json(parent_path / "dataframe_30k_20.json")


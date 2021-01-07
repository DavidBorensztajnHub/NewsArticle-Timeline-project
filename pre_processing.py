import json
import pandas as pd
import numpy as np
import string
import re
import nltk
from pandas.io.json import json_normalize

articles = []
file = open("../articles_en_2019_raw.nosync.json")
i = 0
for article in file:
    articles.append(json.loads(article))
    i = i + 1
    if i >= 500:
        break
file.close()

df_flat = json_normalize(data = articles[0], record_path = 'body', meta = ['id', 'date'])
for i in range(1, len(articles)):
    df = json_normalize(data = articles[i], record_path = 'body', meta = ['id', 'date'])
    df_flat = df_flat.append(df,ignore_index=False, sort=True)

def remove_html_punctuation(text):
    result = string.punctuation  
    text = re.sub('<[^<]+?>', '', text)
    no_punct=[words for words in text if words not in result]
    words_wo_punct=''.join(no_punct)
    return words_wo_punct

df_flat['content_wo_punct'] = df_flat['content'].apply(lambda x: remove_html_punctuation(x))
def tokenize(text):
    split=re.split("\W+",text) 
    return split

df_flat['content_wo_punct_split']=df_flat['content_wo_punct'].apply(lambda x: tokenize(x.lower()))

stopword = nltk.corpus.stopwords.words('english')

def remove_stopwords(text):
    text=[word for word in text if word not in stopword]
    return text
df_flat['content_wo_punct_split'] = df_flat['content_wo_punct_split'].apply(lambda x: remove_stopwords(x))

print(df_flat.head(200))
print("   ")

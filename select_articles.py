# libraries
import json, pandas as pd, numpy as np
import string, re, nltk
from bs4 import BeautifulSoup
from pathlib import Path

df = pd.read_csv("../dataframe2.csv").head(10)

search_terms = ["virus","corona"]
thresh = 2
for article, title in zip(df["intro"],df["header"]):
    counter = 0
    for term in search_terms:
        if term in article:
            counter +=1 
        
        if counter >= thresh:
            print(title)
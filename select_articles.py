# libraries
import pandas as pd, numpy as np
from pathlib import Path

df = pd.read_csv("../dataframe2.csv")

search_terms = ["virus","corona"]
thresh = 2
filter = []
for intro, title in zip(df["intro"],df["header"]):
    num_terms = 0
    for term in search_terms:
        if term in intro:
            num_terms +=1 
        
        filter.append(num_terms >= thresh)
            
df = df.drop(pd.Series(filter),axis=0)
df.to_csv("stuff.csv")
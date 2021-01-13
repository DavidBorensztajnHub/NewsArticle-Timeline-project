# libraries
import pandas as pd, numpy as np
from pathlib import Path
import ast

# load data
df = pd.read_csv("../dataframe2.csv", converters=
{"header":ast.literal_eval,"intro":ast.literal_eval})

# define keywords per topic
virus_terms = ["virus","covid","quarantaine","covid19","lockdown","wuhan","lung"]
formula1 = ["formula","formula1","hamilton","verstappen","botta","albon","grosjean","car","race","grand","prix",
"driver","f1","lewis","mercedes","max","red","bull","ferrari","ricciardo","vettel","gp","mclaren","russell",
"schumacher","lauda","pole"]

def remove_long_intros(df, max=100, col="intro"):
    df.loc[:,col] = df.loc[:,col].str[:max]
    return df

def filter_topic(df, search_terms, thresh):
    filter = []
    for header,intro in zip(df["header"],df["intro"]):
        num_terms = 0
        for term in search_terms:
            if term in header:
                num_terms += 1 
            if term in intro:
                num_terms += 1             
            
        filter.append(num_terms >= thresh)
                
    return df.loc[pd.Series(filter)]

thresh = 3
df = remove_long_intros(df)
df = filter_topic(df, virus_terms, thresh)
print(df)
df.to_csv("../virus.csv")
#df.to_csv("../formula.csv")

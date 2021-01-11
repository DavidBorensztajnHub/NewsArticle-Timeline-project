# libraries
import pandas as pd, numpy as np
from pathlib import Path

df = pd.read_csv("../dataframe2.csv")
search_terms = ["virus","covid","quarantaine","covid19","lockdown","wuhan","lung"]
formula1 = ["formula","formula1","hamilton","verstappen","botta","albon","grosjean","car","race","grand","prix",
"driver","f1","lewis","mercedes","max","red","bull","ferrari","ricciardo","vettel","gp","mclaren","russell",
"schumacher","lauda","pole"]

def filter_topic(df, search_terms, thresh):
    filter = []
    for header,intro in zip(df["header"],df["intro"]):
        num_terms = 0
        for term in search_terms:
            if term in header:
                num_terms += 1 
        
        for term in search_terms:
            if term in intro:
                num_terms += 1 
            
        filter.append(num_terms >= thresh)
                
    return df.loc[pd.Series(filter)]

thresh = 6
filtered_df = filter_topic(df, formula1, thresh)
print(filtered_df.shape)
#filtered_df.to_csv("../filter2.csv")
filtered_df.to_csv("../formula.csv")

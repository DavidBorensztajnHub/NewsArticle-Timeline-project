<<<<<<< HEAD
"""
this program takes the pre processed dataset
and only keeps the articles that are
relevant to the selected topic
"""

# libraries
import pandas as pd, numpy as np
from pathlib import Path

# load data
df = pd.read_json("../dataframe.json")
df = df.fillna("NaN")

# define keywords per topic
virus_terms = ["virus","covid","quarantaine","covid19","lockdown","wuhan","lung"]
formula1_terms = ["formula1","verstappen","botta","albon","grosjean","grandprix","f1","ricciardo","vettel","gp"]
brexit_terms = ["brexit","eurosceptic"]
blm_terms = ["floyd","chauvin","minneapolis","blm","movement","breonna"]
=======
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
>>>>>>> b3ec3964a415cdeda1f577ea337d1a2557091e11

def remove_long_intros(df, max=100, col="intro"):
    df.loc[:,col] = df.loc[:,col].str[:max]
    return df

def filter_topic(df, search_terms, thresh):
    filter = []
<<<<<<< HEAD
    terms_list = []
    for header,intro,text in zip(df["header"],df["intro"],df["text"]):
        article_terms = []
=======
    for header,intro in zip(df["header"],df["intro"]):
>>>>>>> b3ec3964a415cdeda1f577ea337d1a2557091e11
        num_terms = 0
        for term in search_terms:
            if term in header:
                num_terms += 1 
<<<<<<< HEAD
                article_terms.append(term)
            if term in intro:
                num_terms += 1       
                article_terms.append(term)
            #if term in text:
                #num_terms += 1       
                #article_terms.append(term)

        filter.append(num_terms >= thresh)
        terms_list.append(article_terms)
    df["terms"] = terms_list
    return df.loc[pd.Series(filter)]

thresh = 1
df = remove_long_intros(df)
df = filter_topic(df, blm_terms, thresh)
print(df)

#df.to_csv("../virus.csv")
#df.to_csv("../formula.csv")
#df.to_csv("../brexit.csv")
df.to_csv("../blm.csv")


=======
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
>>>>>>> b3ec3964a415cdeda1f577ea337d1a2557091e11

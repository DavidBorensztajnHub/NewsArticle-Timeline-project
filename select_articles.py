"""
this program takes the pre processed dataset
and only keeps the articles that are
relevant to the selected topic
"""

# libraries
import pandas as pd, numpy as np
from pathlib import Path

# load data
df = pd.read_csv("../dataframe2_key.csv")
df = df.fillna("NaN")
df_wiki = pd.read_csv("../wiki_df.csv")

# define keywords per topic
virus_terms = ["virus","covid","quarantaine","covid19","lockdown","wuhan","lung"]
formula1_terms = ["formula1","verstappen","botta","albon","grosjean","grandprix","f1","ricciardo","vettel","gp"]
brexit_terms = ["brexit","eurosceptic"]
blm_terms = ["floyd","chauvin","minneapolis","blm","movement","breonna"]
blm = df_wiki['blm_top_1']
print(blm)
def remove_long_intros(df, max=100, col="intro"):
    df.loc[:,col] = df.loc[:,col].str[:max]
    return df

def filter_topic(df, search_terms, thresh):
    filter = []
    terms_list = []
    for header,intro,text,top_words in zip(df["header"],df["intro"],df["text"], df["top_words"]):
        article_terms = []
        num_terms = 0
        for term in ", ".join(map(str, search_terms)):
            print(term)
            # if term in header:
            #     num_terms += 1 
            #     article_terms.append(term)
            # if term in intro:
            #     num_terms += 1       
            #     article_terms.append(term)
            # if term in text:
            #     num_terms += 1       
            #     article_terms.append(term)
            if term in top_words[0]:
                num_terms += 1
                article_terms.append(term)
        filter.append(num_terms >= thresh)
        terms_list.append(article_terms)
    df["terms"] = terms_list
    filter = pd.Series(filter).values
    return df.loc[filter]

thresh = 1
#df = remove_long_intros(df)ß
df = filter_topic(df, blm, thresh)
print(df.head())

#df.to_csv("../virus.csv")
#df.to_csv("../formula.csv")
#df.to_csv("../brexit.csv")
df.to_csv("../blm.csv")

#df_wiki['blm_top_1'][0].split(",")
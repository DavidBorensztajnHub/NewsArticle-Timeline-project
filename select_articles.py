"""
this program takes the pre processed dataset
and only keeps the articles that are
relevant to the selected topic
"""

# libraries
import pandas as pd, numpy as np
from pathlib import Path

# function that only keeps 100 first words of intros
def remove_long_intros(df, max=100, col="intro"):
    df.loc[:,col] = df.loc[:,col].str[:max]
    return df

# load data

df = pd.read_json("../dataframe_200k.json")
df = remove_long_intros(df)
wiki_df = pd.read_json("../wiki_df.json")

# use common wikipedia words to find keywords per topic
#covid_terms_original = ["virus","covid","quarantaine","covid19","lockdown","wuhan","lung"]
covid_terms = {1:wiki_df.loc["covid","top_1"],
                2:[x.split(" ") for x in wiki_df.loc["covid","top_2"]],
                3:[x.split(" ") for x in wiki_df.loc["covid","top_3"]]}
#f1_terms_original = ["formula1","verstappen","botta","albon","grosjean","grandprix","f1","ricciardo","vettel","gp"]
f1_terms = {1:wiki_df.loc["f1","top_1"],
                2:[x.split(" ") for x in wiki_df.loc["f1","top_2"]],
                3:[x.split(" ") for x in wiki_df.loc["f1","top_3"]]}
#bxt_terms_original = ["brexit","eurosceptic"]
bxt_terms = {1:wiki_df.loc["bxt","top_1"],
                2:[x.split(" ") for x in wiki_df.loc["bxt","top_2"]],
                3:[x.split(" ") for x in wiki_df.loc["bxt","top_3"]]}
#blm_terms_original = ["floyd","chauvin","minneapolis","blm","movement","breonna"]
blm_terms = {1:wiki_df.loc["blm","top_1"],
                2:[x.split(" ") for x in wiki_df.loc["blm","top_2"]],
                3:[x.split(" ") for x in wiki_df.loc["blm","top_3"]]}

impeach_terms = {1:wiki_df.loc["impeach","top_1"],
                2:[x.split(" ") for x in wiki_df.loc["impeach","top_2"]],
                3:[x.split(" ") for x in wiki_df.loc["impeach","top_3"]]}



# manually change it a bit
covid_terms[2][2] = ["global","pandemic"]

f1_terms[2][2] = ["lewis","hamilton"]
f1_terms[2][3] = ["formula","one"]
f1_terms[2][4] = ["max","verstappen"]

bxt_terms[2][0] = ["transition","period"]
bxt_terms[3][0] = ["withdraw","united","kingdom"]
del bxt_terms[3][1:]
blm_terms[1][3] = "floyd"
blm_terms[1][4] = "breonna"
blm_terms[2][2] = ["george","floyd"]
blm_terms[2][3] = ["breonna","taylor"]
blm_terms[2][4] = ["movement","black"]

impeach_terms[1][0] = "trial"
impeach_terms[1][4] = "committee"
impeach_terms[2][2] = ["trump", "trial"]
impeach_terms[2][4] = ["impeachment", "trump"]
impeach_terms[2][0] = ["impeachment", "committee"]
impeach_terms[1][2] = "impeached"
del impeach_terms[1][3]




print(impeach_terms)
# this function only keeps the relevant articles in the dataframe
def filter_topic(df, col, search_terms, thresh):
    filter = []
    terms_list = []
    # loop through articles
    for header, intro in zip(df["header"],df[col]):
        word_list = header + intro
        article_terms = []
        score = 0
        # loop through words in article
        for word1, word2, word3 in zip(word_list,word_list[1:],word_list[2:]):            
            # single words
            for term in search_terms[1]:
                if word1 == term:
                    if term not in article_terms:
                        score += 1
                        article_terms.append(term)
            # 2 words
            for term1, term2 in search_terms[2]:
                if term1 == word1 and term2 == word2: 
                    if (term1,term2) not in article_terms:
                        score += 2
                        article_terms.append((term1,term2))
            # 3 words
            for term1, term2, term3 in search_terms[3]:
                if term1 == word1 and term2 == word2 and term3 == word3:
                    if (term1,term2,term3) not in article_terms:
                        score += 2
                        article_terms.append((term1,term2,term3))
        if article_terms == []:
            article_terms.append(score)
            article_terms.append(None)
        # keep articles with sufficiently high score
        filter.append(score >= thresh)
        #if score > thresh: print(score)
        terms_list.append(article_terms)
    df["terms"] = terms_list

    return df[filter]

# filter articles
thresh = 3


df = filter_topic(df, "intro", bxt_terms, thresh)
print(f"Kept {df.shape[0]} articles")


# df.to_json("../covid.json")
# df.to_json("../f1.json")
df.to_json("../bxt.json")
#df.to_json("../blm.json")
#df.to_json("../blm.json")

#df.to_csv("../covid.csv")
#df.to_csv("../f1.csv")
df.to_csv("../bxt.csv")
#df.to_csv("../blm.csv")
# df.to_csv("../impeach.csv")
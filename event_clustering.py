#libraries
import pandas as pd
import numpy as np
from pathlib import Path
from tqdm import tqdm
import spacy
from sklearn.cluster import DBSCAN, KMeans, OPTICS
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer


# load data
df = pd.read_json("../covid.json")

# vectorization
nlp = spacy.load('en_core_web_lg')  
df["str_header"] = [" ".join(x) for x in df.header]
df["str_intro"] = [" ".join(x) for x in df.intro]

tfidf_vectorizer = TfidfVectorizer()
df.drop_duplicates(subset="str_header",keep=False,inplace=True)
df.drop_duplicates(subset="str_intro",keep="first",inplace=True)


# df["vectors"] = [tfidf_vectorizer.fit_transform(x) for x in df["str_text"]]

# vectors = np.array([x for x in df["vectors"]])

vectors = tfidf_vectorizer.fit_transform(df["str_intro"]) #fit the vectorizer to synopses

#n_classes = {}
# for i in tqdm(np.arange(0.001, 1, 0.002)):
#     dbscan = DBSCAN(eps = i, min_samples=2, metric="cosine", ).fit(x)
#     n_classes.update({i: len(pd.Series(dbscan.labels_).value_counts())})

# A high ratio stands for good clustering
epsilist = []
percentage_list = []
def check_onedate(cluster):
    if len(cluster.date.value_counts()) == 1:
        return 1
    else:
        return 0

for i in tqdm(np.arange(0.001, 1, 0.002)):
    dbscan = DBSCAN(eps = i, min_samples=2, metric="cosine", ).fit(vectors)
    results_df = pd.DataFrame({"label":dbscan.labels_, "sent":df["str_header"], "date":df["date"]})
    nr_clusters = len(pd.Series(dbscan.labels_).value_counts())
    clusters_df = results_df[results_df.label != -1]
    single_date_count = 0
    for cluster in range(nr_clusters - 1):
        c = clusters_df[clusters_df["label"] == cluster]
        single_date_count += check_onedate(c)
    if nr_clusters == 1:
        nr_clusters += 1
    percentage = single_date_count / (nr_clusters - 1)
    percentage_list.append(percentage)
    epsilist.append(i)


plt.plot(epsilist, percentage_list)
plt.show()

dbscan = DBSCAN(eps = 0.175, min_samples=3, metric="cosine", ).fit(vectors)
results_df = pd.DataFrame({"label":dbscan.labels_, "sent":df["str_header"], "date":df["date"]})

# amount_clusters = len(pd.Series(dbscan.labels_).value_counts())
# clusters_df = results_df[results_df.label != -1]

# amount_dates = len(clusters_df["date"].value_counts())
# ratio = nr_clusters / number_dates

results_df.to_csv("../covid_events.csv", index=False)
#print(kmeans.inertia_)

"""
# elbow
errors = []

for n in range(50,400,5):
    kmeans = KMeans(n_clusters=100).fit(vectors)
    errors.append(kmeans.inertia_)
plt.plot([n for n in range(50,400,5)],errors)
plt.show()
"""
#libraries
import pandas as pd, numpy as np
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

dbscan = DBSCAN(eps = 0.05, min_samples=2, metric="cosine", ).fit(vectors)
# optics = OPTICS(min_samples=2,  metric="cosine").fit(vectors)

kmeans = KMeans(n_clusters=25).fit(vectors)

results = pd.DataFrame({"label":dbscan.labels_, "sent":df["str_header"], "date":df["date"]})

results.to_csv("../covid_events.csv", index=False)
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
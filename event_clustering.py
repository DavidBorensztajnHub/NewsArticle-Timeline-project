#libraries
import pandas as pd, numpy as np
from pathlib import Path
from tqdm import tqdm
import spacy
from sklearn.cluster import DBSCAN, KMeans
import matplotlib.pyplot as plt

# load data
df = pd.read_json("../preproc_data/dataframe_10k_20.json")

# vectorization
nlp = spacy.load('en_core_web_lg')  

df["str_text"] = [" ".join(x) for x in df.header]
df["vectors"] = [nlp(x).vector for x in df["str_text"]]

vectors = np.array([x for x in df["vectors"]])

#n_classes = {}
# for i in tqdm(np.arange(0.001, 1, 0.002)):
#     dbscan = DBSCAN(eps = i, min_samples=2, metric="cosine", ).fit(x)
#     n_classes.update({i: len(pd.Series(dbscan.labels_).value_counts())})

#dbscan = DBSCAN(eps = 0.04, min_samples=2, metric="cosine", ).fit(vectors)
kmeans = KMeans(n_clusters=1000).fit(vectors)

results = pd.DataFrame({"label":kmeans.labels_, "sent":df["str_text"], "date":df["date"]})

results.to_csv("../events.csv", index=False)
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
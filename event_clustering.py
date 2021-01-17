#libraries
import pandas as pd, numpy as np
from pathlib import Path
from tqdm import tqdm
import spacy
import numpy as np
from sklearn.cluster import DBSCAN


# load data
df = pd.read_json("../covid.json")

#vectorization
nlp = spacy.load('en_core_web_lg')

sent_vecs = {}
docs = []

for intro in tqdm(df.intro):
    str_intro = " ".join(intro)

    doc = nlp(str_intro)
    docs.append(doc)
    sent_vecs.update({str_intro: doc.vector})

sentences = list(sent_vecs.keys())
vectors = list(sent_vecs.values())

x = np.array(vectors)
n_classes = {}
# for i in tqdm(np.arange(0.001, 1, 0.002)):
#     dbscan = DBSCAN(eps = i, min_samples=2, metric="cosine", ).fit(x)
#     n_classes.update({i: len(pd.Series(dbscan.labels_).value_counts())})

dbscan = DBSCAN(eps = 0.055, min_samples=2, metric="cosine", ).fit(x)

results = pd.DataFrame({"label": dbscan.labels_ , "sent": sentences})


pd.DataFrame.to_csv(results, "../events.csv", index=False)

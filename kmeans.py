import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from tqdm import tqdm
import matplotlib.pyplot as plt
cv = CountVectorizer()
df = pd.read_json("../covid.json")


detokenized = []
for intro in df['intro']:
    detokenize = " ".join(intro)
    detokenized.append(detokenize)


X = cv.fit_transform(detokenized)

wcss = []

for i in tqdm(range(1,1000)):
    kmeans = KMeans(n_clusters = i, init='k-means++',max_iter = 300, n_init = 10, random_state = 0, verbose = True)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)

plt.plot(range(1,1000),wcss)
plt.title('elbow method')
plt.xlabel('no of clusters')
plt.ylabel('wcss')
plt.show()

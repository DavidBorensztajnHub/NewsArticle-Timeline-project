import json
import pandas as pd
import numpy as np
from pathlib import Path

def open_json(filepath):
    articles = []
    file = open(filepath)
    i=0
    for article in file:
        articles.append(json.loads(article))
        i+=1
        if i > 10: break
    file.close()
    return articles

parent_path = Path.cwd().parent
articles = open_json(parent_path / "articles_en_2020_raw.json")

dates = [article["date"] for article in articles]
bodies = [article["body"] for article in articles]

def unpack_bodies(bodies):
    pass

df = pd.DataFrame({"date":dates, "body":bodies})
print(df)
df.to_csv(parent_path / "dataframe2.csv")


import json
import pandas as pd
import numpy as np
from pathlib import Path

parent_path = Path.cwd().parent
articles = []
file = open(parent_path / "articles_en_2020_raw.json")
for article in file:
    articles.append(json.loads(article))
file.close()

dates = [article["date"] for article in articles]
bodies = [article["body"] for article in articles]

df = pd.DataFrame({"date":dates, "body":bodies})
df.to_csv(parent_path / "dataframe.csv")


import json
import pandas as pd

articles = []
file = open("articles_en_2020_raw.json")
for article in file:
    articles.append(json.loads(article))
file.close()

dates = [article["date"] for article in articles]
bodies = [article["body"] for article in articles]

df = pd.DataFrame({"date":dates,"body":bodies})

df.head()

for i in articles[0]:
    print(i)

print(articles[2]["images"])


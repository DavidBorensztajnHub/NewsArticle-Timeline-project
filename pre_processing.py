import json
import pandas as pd
import numpy as np


articles = []
file = open("../articles_en_2019_2020_raw/articles_en_2020_raw.json")
i = 0
for article in file:
    articles.append(json.loads(article))
    i = i + 1
    if i >= 50:
        break
file.close()
if articles[2]["body"][3]["type"] == "p":
    print("yesss")

bodylens = []
for article in articles:
    bodylens.append(len(article["body"]))
bodylens = np.array(bodylens)

small_articles = np.where(bodylens < 5)[0]
articles = np.array(articles)
articles = np.delete(articles, small_articles)
articles = articles.tolist()

print(len(articles))

dates = [article["date"] for article in articles]
titles = [article["body"][0]["content"] if article["body"][0]["type"] == 'hl1' else "n/a" for article in articles]
undertitles = [article["body"][1]["content"] if article["body"][1]["type"] == 'hl2' else article["body"][2]["content"] if article["body"][2]["type"] == 'hl2' else article["body"][3]["content"] if article["body"][3]["type"] == 'hl2' else "n/a" for article in articles]
intros = [article["body"][1]["content"] if article["body"][1]["type"] == 'intro' else article["body"][2]["content"] if article["body"][2]["type"] == 'intro' else article["body"][3]["content"] if article["body"][3]["type"] == 'intro' else "n/a" for article in articles]
authors = [article["body"][1]["content"] if article["body"][1]["type"] == 'byline' else article["body"][2]["content"] if article["body"][2]["type"] == 'byline' else article["body"][3]["content"]if article["body"][3]["type"] == 'byline' else "n/a" for article in articles]
firstp = [article["body"][1]["content"] if article["body"][1]["type"] == 'p' else article["body"][2]["content"] if article["body"][2]["type"] == 'p' else article["body"][3]["content"] if article["body"][3]["type"] == 'p' else article["body"][4]["content"] if article["body"][4]["type"] == 'p' else article["body"][5]["content"] if article["body"][5]["type"] == 'p' else "n/a" for article in articles]

bodies = [article["body"][1:] for article in articles]



df = pd.DataFrame({"date":dates, "author":authors, "title":titles, "undertitle":undertitles, "intro":intros, "firstp":firstp, "body":bodies})
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(df)



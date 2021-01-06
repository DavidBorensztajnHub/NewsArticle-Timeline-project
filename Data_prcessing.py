import json


articles = []
file = open("/content/drive/MyDrive/Leren&Beslissen/Datasets/articles_en_2019_2020_raw/articles_en_2019_raw.json")
for article in file:
    articles.append(json.loads(article))
file.close()

print(articles[1]["body"][7]["content"])
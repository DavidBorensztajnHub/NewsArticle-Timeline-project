import gensim, pandas as pd, numpy as np

df = pd.read_json("../covid_30k.json")
words=["covid","coronavirus","corona","pandemic","virus"]
df["header"] = [[y for y in x if y not in words] for x in df["header"]]


dictionary = gensim.corpora.Dictionary(df.header)
dictionary.filter_extremes(no_below=3, no_above=.5)
bag_of_words = [dictionary.doc2bow(header) for header in df.header] 

tfidf_model = gensim.models.TfidfModel(bag_of_words)
headers_tfidf = tfidf_model[bag_of_words]

# multicore werkt niet op mijn computer, weet niet waarom
lda_model = gensim.models.LdaModel(headers_tfidf,num_topics=30,
id2word=dictionary,passes=3)

article_num = 16
print(df.iloc[article_num,:])
for index, score in sorted(lda_model[bag_of_words[article_num]], key=lambda tup: -1*tup[1]):
    print("\nScore: {}\t \nTopic: {}".format(score, lda_model.print_topic(index, 10)))
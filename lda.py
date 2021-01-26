import gensim, pandas as pd, numpy as np, matplotlib.pyplot as plt


# multicore werkt niet op mijn computer, weet niet waarom
"""
lda_model = gensim.models.LdaModel(headers_tfidf,num_topics=10,
id2word=dictionary,passes=3)

lda_model2 = gensim.models.LdaModel(bag_of_words,id2word=dictionary,passes=3)

article_num = 16
print(df.iloc[article_num,:])
for index, score in sorted(lda_model[bag_of_words[article_num]], key=lambda tup: -1*tup[1]):
    print("\nScore: {}\t \nTopic: {}".format(score, lda_model.print_topic(index, 10)))

for idx, topic in lda_model2.print_topics(-1):
    print('Topic: {} \nWords: {}'.format(idx, topic))
"""

def compute_coherence_values(dictionary, bow, texts, limit, start=2, step=3):
    coherence_values = []
    model_list = []
    for num_topics in range(start, limit, step):
        model = gensim.models.LdaModel(bow, id2word=dictionary)
        model_list.append(model)
        coherencemodel = gensim.models.CoherenceModel(model=model, texts=texts, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())

    return model_list, coherence_values

def main():

    df = pd.read_json("../covid_75k.json")
    words=["covid","coronavirus","corona","pandemic","virus"]
    df["header"] = [[y for y in x if y not in words] for x in df["header"]]

    dictionary = gensim.corpora.Dictionary(df.header)
    #dictionary.filter_extremes(no_below=3, no_above=.5)
    bag_of_words = [dictionary.doc2bow(header) for header in df.header] 

    #tfidf_model = gensim.models.TfidfModel(bag_of_words)
    #headers_tfidf = tfidf_model[bag_of_words]

    # Can take a long time to run.
    model_list, coherence_values = compute_coherence_values(dictionary, bag_of_words, df.header.to_list(), start=50, limit=1000, step=25)

    # Show graph
    limit=1000; start=50; step=25;
    x = range(start, limit, step)
    plt.plot(x, coherence_values)
    plt.xlabel("Num Topics")
    plt.ylabel("Coherence score")
    plt.legend(("coherence_values"), loc='best')
    plt.show()

    # Print the coherence scores
    for m, cv in zip(x, coherence_values):
        print("Num Topics =", m, " has Coherence Value of", round(cv, 4))

if __name__ == "__main__":
    main()

import nltk
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

def lemmatizer_stemmer(text):
    lemmatizer = WordNetLemmatizer()
    ps = PorterStemmer()
    if text:
        text=[ps.stem(lemmatizer.lemmatize(word)) for word in text]
        return text

f1_words = ['formula', 'hamilton', 'verstappen', 'botta', 'albon', 'grosjean', 'car', 'race', 'grand', 'prix', 'driver', 'f1', 'lewi', 'merced', 'max', 'red', 'bull', 'ferrari', 'ricciardo', 'vettel', 'gp', 'mclaren', 'russel', 'schumach', 'lauda', 'pole', 'formula1']

print(lemmatizer_stemmer(f1_words))
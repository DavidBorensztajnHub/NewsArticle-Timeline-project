"""
takes html from urls (to wikipedia pages),
extracts the words and stores them in text files
"""

import re
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords

parent_path = Path.cwd().parent

def html2text(html):
    soup = BeautifulSoup(html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    stop_words = set(stopwords.words("english"))

    # remove punctuation
    text = re.sub('[^a-zA-Z]', ' ', text)

    # convert to lowercase
    text = text.lower()

    # remove tags
    text=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text)

    # remove special characters and digits
    text=re.sub("(\\d|\\W)+"," ",text)

    # convert to list from string
    text = text.split()

    # stemming
    ps=PorterStemmer()    #Lemmatisation
    lem = WordNetLemmatizer()
    text = [lem.lemmatize(word) for word in text if not word in  
            stop_words] 
    text = " ".join(text)
    return text

# urls
urls = {"covid":"https://en.wikipedia.org/wiki/Coronavirus_disease_2019",
"blm":"https://en.wikipedia.org/wiki/Black_Lives_Matter",
"bxt":"https://en.wikipedia.org/wiki/Brexit","f1":"https://en.wikipedia.org/wiki/Formula_One", "impeach": "https://en.wikipedia.org/wiki/First_impeachment_of_Donald_Trump"}

# apply function
for topic, url in urls.items():
    # get text from urls
    request = requests.get(url)
    text = html2text(request.text)

    # add text to file
    file = open(f"../wiki_{topic}.txt","w")
    file.write(text)
    file.close()
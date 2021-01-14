import re, nltk
from urllib.request import urlopen
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
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    stop_words = set(stopwords.words("english"))

    #Remove punctuations
    text = re.sub('[^a-zA-Z]', ' ', text)

    #Convert to lowercase
    text = text.lower()

    #remove tags
    text=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text)

    # remove special characters and digits
    text=re.sub("(\\d|\\W)+"," ",text)

    ##Convert to list from string
    text = text.split()

    ##Stemming
    ps=PorterStemmer()    #Lemmatisation
    lem = WordNetLemmatizer()
    text = [lem.lemmatize(word) for word in text if not word in  
            stop_words] 
    text = " ".join(text)
    return text

#apply function
url_covid = "https://en.wikipedia.org/wiki/Coronavirus_disease_2019"
html_covid = urlopen(url_covid).read()
text_covid = html2text(html_covid)

url_blm = "https://en.wikipedia.org/wiki/Black_Lives_Matter"
html_blm = urlopen(url_blm).read()
text_blm = html2text(html_blm)

url_bxt ="https://en.wikipedia.org/wiki/Brexit"
html_bxt = urlopen(url_bxt).read()
text_bxt = html2text(html_bxt)

url_f1 = "https://en.wikipedia.org/wiki/Formula_One"
html_f1 = urlopen(url_f1).read()
text_f1 = html2text(html_f1)

# safe text
file2write=open(parent_path / "wiki_corona.txt",'w')
file2write.write(text_covid)
file2write.close()

file2write=open(parent_path / "wiki_blm.txt",'w')
file2write.write(text_blm)
file2write.close()

file2write=open(parent_path / "wiki_bxt.txt",'w')
file2write.write(text_bxt)
file2write.close()

file2write=open(parent_path / "wiki_f1.txt",'w')
file2write.write(text_f1)
file2write.close()


# Machine-Geleerden

### <span style="color:blue">What each document does</span>

**pre_processing.py**
> This program loads the json dataset and \
preprocesses the data by removing irrelevant \
words and punctuation.it then stores the \
data in a .csv file

**select_articles.py**
> this program takes the pre processed dataset \
and only keeps the articles that are \
relevant to the selected topic

**html2text.py**
> takes html from urls (to wikipedia pages), \
extracts the words and stores them in text files

**clean_key.py**
> takes as input either the filtered dataset \
or the wikipedia text files and finds \
the most common word combinations \
(of 1, 2 and 3 words)

**wordnet.py**
> geen idee waarvoor dit is

**find_article.py**
> this function selects an article from the \
raw data and writes its body to a text file

### <span style="color:blue">Necessary libraries</span>
* `import pandas`
* `import numpy`
* `from bs4 import BeautifulSoup`
* `import nltk` (and download english dataset)
* `from pathlib import Path`
* `import sklearn`
* `import requests`

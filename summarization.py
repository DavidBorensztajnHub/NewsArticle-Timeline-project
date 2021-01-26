import gensim
from gensim.summarization import summarize

text = open("summmaa.txt")
line = text.read()
short_summary = summarize(line, ratio=0.01)
print(short_summary)
text.close()
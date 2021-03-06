"""
this function selects an article from the 
raw data and writes its body to a text file
"""

import json

def find_article(filename, index):
    file = open(filename)
    i=0
    for line in file:
        if i == index:
            article = json.loads(line)
            break
        i+=1
    file.close()

    file = open("../body.txt","w")
    file.write(str(article["body"]))
    file.close()

index = 40
find_article("../articles_en_2020_raw.json", index)

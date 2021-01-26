def remove_wikipedia_crap(text):
    wikiwords = ["archived ", "archived original ", "retrieved january ",  "retrieved ", "retrieved ", "article ", "edit" "january ", "february ", "march ", "april ", "may ", "june ", "july ", "august ", "september ", "oktober ", "november ", "december "]
    for word in wikiwords:
        text = text.replace(word, "")
    return [text]


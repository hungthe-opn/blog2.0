import re

with open("bad_words.txt") as f:
    ls = list()
    for i in f:
        ls.append(i)


def comment_filter(body: str) -> str:
    for idx, word in enumerate(ls):
        body = body.replace(word, '*'*len(word))
    return body
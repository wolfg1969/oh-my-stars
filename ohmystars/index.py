import re

__author__ = 'guoyong'

REPO_NAME_PATTERN = re.compile("[_\-]")
REPO_DESC_PATTERN = re.compile("[\s_\-]")


def calculate_ngrams(word, n):  # https://en.wikipedia.org/wiki/N-gram
    return [u''.join(gram) for gram in zip(*[word[i:] for i in range(n)])]


def split_repo_name(name):
    return REPO_NAME_PATTERN.split(name)


def split_repo_desc(desc):
    return REPO_DESC_PATTERN.split(desc)


def split_keywords(keywords):
    ret = []
    for keyword in keywords:
        for n in range(2, len(keyword) + 1):
            for word in calculate_ngrams(keyword, n):
                ret.append(word)
    return ret


def update_inverted_index(index, key, *items):
    existing = index.get(key, [])
    existing += items
    index[key] = list(set(sorted(existing)))


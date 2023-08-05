import re


# https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
def to_kebab(word):
    word = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', word)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', word).lower()
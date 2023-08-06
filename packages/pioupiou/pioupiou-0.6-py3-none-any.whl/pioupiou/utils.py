from nameme import NameMe
from nameme.adjectives import adjective_words
from nameme.nouns import noun_words


def generate_name() -> str:
    name = NameMe(adjective_words, noun_words, seperator="-")
    return name.get_name()

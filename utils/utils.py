from utils.consts import *
from newspaper import Article
from tldextract import extract


# region parser

def parse_article_nltk(url: str) -> Article:
    """
    Parses the article url to Article object with nlp/nltk parameters.

    :param url: url of the given article
    :return: parsed nltk/nlp Article object
    """
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()

    return article


def calculate_time_to_read(text: str) -> int:
    """
    Calculates read time with the average read time of {X} WPM
    From the given article text
    :param text: the article text
    :return: read time in minutes
    """
    return len(text.split()) // WORDS_PER_MINUTE


def parse_source_site_from_url(url: str) -> str:
    """
    Extracting the name of the site from the whole url
    :param url: url of a given article
    :return: the name of the domain
    Example - http://www.medicinenet.com/script/main/art.asp?articlekey=248973 -> medicinenet
    """
    return extract(url).domain

# endregion

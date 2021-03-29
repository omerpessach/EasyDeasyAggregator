import feedparser
import time
from .consts import *
from newspaper import Article
from tldextract import extract
from attrdict import AttrDict
import requests
from .data_sources import data_django_feed


class Feed:
    """
    Represents feed item
    """

    def __init__(self, feed_dict: dict):
        self.missing_fields = None  # Missing fields that aggregator needs to fill
        self.source_site = None  # Source site of the feed
        self.entries = None  # The actual articles entries
        self.title = None  # The title of the feed itself

        self.parse_feed_params(feed_dict)

    def parse_feed_params(self, feed_dict: dict) -> None:
        """
        Parsing the feed values to the instance object upon creation
        """
        feed_data = feedparser.parse(feed_dict[URL])

        self.missing_fields = feed_dict[MISSING_FIELDS].split(',')
        self.source_site = feed_dict[WEBSITE]
        self.title = feed_data.feed.title
        self.entries = feed_data.entries

    def __str__(self):
        return self.title


class Aggregator:
    """
    Responsible for aggregating data and updating the server with the newest articles and researches!
    """

    def __init__(self):
        self._feeds = None  # the aggregator feeds that needs to be aggregated

    def aggregate(self):
        """
        Main function of the aggregator, it loops through all the updated feeds and aggregates the information!
        """
        self.update_feeds()

        for feed_dict in self._feeds:
            """
            Looping through all the feeds, each feed is dict from the API response
            """
            feed = Feed(feed_dict)

            print(feed)

            for entry in feed.entries:
                """
                Flow per entry:
                parsing the entry default params -> parsing the complicated params -> filling missing fields -> POSTing
                """
                entry_url = entry.link

                article = self.parse_article_nltk(entry_url)

                title = entry.title
                parsed_date = entry.published_parsed
                time_to_read = self.calculate_time_to_read(article.text)

                """ changing the date format to what we use on django side."""
                published_date = time.strftime(DATE_FORMAT, parsed_date)

                summary = article.summary if MISSING_SUMMARY in feed.missing_fields else entry.description
                source_site_name = self.parse_source_site_from_url(entry_url)

                """ POSTing the data """
                self.post_article(AttrDict({
                    TITLE: title,
                    URL: entry_url,
                    SUMMARY: summary,
                    TIME_TO_READ: time_to_read,
                    SOURCE_SITE: source_site_name,
                    DISEASES: ['test_disease'],  # TODO - replace with real diseases
                    PUBLISHED_DATA: published_date
                }))

    # region sender

    @staticmethod
    def post_article(article_data: AttrDict):
        """
        Packs the article data and POSTs it to the server

        * must have all the data before POSTing *
        """
        post_data = {
            TITLE: article_data.title,
            URL: article_data.url,
            SUMMARY: article_data.summary,
            TIME_TO_READ: article_data.time_to_read,
            SOURCE_SITE: article_data.source_site,
            DISEASES: article_data.diseases,
            PUBLISHED_DATA: article_data.published_date
        }

        print(ARTICLE_DATA_PRINT.format(article_data.title,
                                        article_data.url,
                                        article_data.published_date,
                                        article_data.source_site,
                                        article_data.time_to_read,
                                        article_data.diseases))

        response = requests.post(ARTICLES_URL, post_data)

        print_message = SUCCESSFUL_POST_PRINT if response.ok else ERROR_PRINT

        print(print_message)

    # endregion

    # region receiver

    def update_feeds(self):
        """
        Updates the aggregator feeds values!
        """
        self._feeds = data_django_feed

    # endregion

    # region parser

    @staticmethod
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

    @staticmethod
    def calculate_time_to_read(text: str) -> int:
        """
        Calculates read time with the average read time of {X} WPM
        From the given article text
        :param text: the article text
        :return: read time in minutes
        """
        return len(text.split()) // WORDS_PER_MINUTE

    @staticmethod
    def parse_source_site_from_url(url: str) -> str:
        """
        Extracting the name of the site from the whole url
        :param url: url of a given article
        :return: the name of the domain
        Example - http://www.medicinenet.com/script/main/art.asp?articlekey=248973 -> medicinenet
        """
        return extract(url).domain

    # endregion
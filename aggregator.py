import feedparser
import time
from .consts import *
from newspaper import Article
from tldextract import extract


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

        :param feed_dict:
        :return:
        """
        feed_data = feedparser.parse(feed_dict[URL])

        self.missing_fields = feed_dict[MISSING_FIELDS].split(',')
        self.source_site = feed_dict[WEBSITE]
        self.title = feed_data.feed.title
        self.entries = feed_data.entries


class Aggregator:
    """
    Responsible for aggregating data and updating the server with the newest articles and researches!
    """

    def __init__(self):
        self._feeds = None  # todo

    def aggregate(self):
        """
        todo
        """
        self.update_feeds()

        for feed_dict in self._feeds:
            """
            """
            feed = Feed(feed_dict)

            print(feed.title)

            for entry in feed.entries:
                """
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

    # region receiver

    def update_feeds(self):
        """
        todo
        """

    # endregion

    # region parser

    @staticmethod
    def parse_article_nltk(url: str) -> Article:
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


def aggregate():
    data = get_feeds_from_server()

    # item is a whole rss feed
    for item in data:
        missing_fields = item[MISSING_FIELDS].split(COMMA)
        source_site_name = item[WEBSITE]

        d = feedparser.parse(item[URL])
        entries = d.entries
        print(d.feed.title + '\n')

        # reading the articles
        for entry in entries:
            url = entry.link

            # newspaper3k init
            article = parse_article_nltk(url)

            title = entry.title
            parsed_date = entry.published_parsed

            # changing the date format to what we use on django side.
            published_date = time.strftime(DATE_FORMAT, parsed_date)

            # special data
            if MISSING_SUMMARY in missing_fields:
                summary = article.summary
            else:
                summary = entry.description

            time_to_read = calculate_time_to_read(article.text)

            if MISSING_WEBSITE in missing_fields:
                source_site_name = parse_source_site_from_url(url)

            # INFO - make sure the pre-coded values are in the DB! (aka 'test_disease')
            # POSTing the data
            post_article({
                TITLE: title,
                URL: url,
                SUMMARY: summary,
                TIME_TO_READ: time_to_read,
                SOURCE_SITE: source_site_name,
                DISEASES: ['test_disease'],  # TODO - replace with real diseases
                PUBLISHED_DATA: published_date
            })

        print('\n')


if __name__ == '__main__':
    aggregate()

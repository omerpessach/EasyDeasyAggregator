import feedparser
import time
from .consts import *


class Feed:
    """
    Represents feed item
    """

    def __init__(self, feed_dict: dict):
        self.missing_fields = None  # todo
        self.source_site = None  # todo
        self.entries = None  # todo
        self.title = None

        self.parse_feed_params(feed_dict)

    def parse_feed_params(self, feed_dict: dict):
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
        self.feeds = None  # todo

    def aggregate(self):
        """
        todo
        """
        self.update_feeds()

        for feed_dict in self.feeds:
            feed = Feed(feed_dict)

    # region receiver

    def update_feeds(self):
        """
        todo
        """

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

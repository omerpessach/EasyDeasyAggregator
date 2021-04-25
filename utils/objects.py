import feedparser
import time
from utils.schemas import EntrySchema
from pprint import pformat
from utils.utils import calculate_time_to_read, parse_article_nltk, parse_source_site_from_url
from utils.consts import *
from requests import HTTPError, ConnectionError
import requests


class Feed:
    """
    Represents feed item
    """

    def __init__(self, feed_dict: dict):
        self.title = None  # The title of the feed itself
        self.missing_fields = None  # Missing fields that aggregator needs to fill
        self.source_site = None  # Source site of the feed
        self.entries = None  # The actual articles entries

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


class Entry:
    """
    Represents entry item
    """

    schema = EntrySchema

    def __init__(self, entry_data):
        self.as_article = None  # entry parsed as Article object

        self.title = None  # title of the entry
        self.url = None  # url of the entry
        self.date = None  # published date of the entry
        self.time_to_read = None  # time it takes to read the entry
        self.summary = None  # description/summary of the entry
        self.site = None  # the source website name
        self.article_data = None  # the complete article data dict

        self.parse_entry_params(entry_data)

    def parse_entry_params(self, entry_data) -> None:
        """
        Parsing the entry values to the instance object upon creation
        """
        self.url = entry_data.link

        self.as_article = parse_article_nltk(self.url)

        self.site = parse_source_site_from_url(self.url)
        self.title = entry_data.title
        self.date = time.strftime(DATE_FORMAT, entry_data.published_parsed)
        self.time_to_read = calculate_time_to_read(self.as_article.text)
        self.summary = self.as_article.summary

        self.article_data = self.schema().load({
            TITLE: self.title,
            URL: self.url,
            SUMMARY: self.summary,
            TIME_TO_READ: self.time_to_read,
            SOURCE_SITE: self.site,
            DISEASES: ['test_disease'],  # TODO - replace with real diseases
            PUBLISHED_DATE: self.date
        })

    def post(self):
        """
        Posts the entry to the server
        """
        print(f'POSTing - \n{self}\n')

        try:
            response = requests.post(ARTICLES_URL, self.article_data)
            response.raise_for_status()
        except (HTTPError, ConnectionError) as e:
            print(e)

    def __str__(self):
        return pformat(self.article_data)

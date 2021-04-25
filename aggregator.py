from utils.consts import *
import requests
from utils.data_sources import data_django_feed
from requests import HTTPError, ConnectionError
from utils.objects import Feed, Entry


class Aggregator:
    """
    Responsible for aggregating data and updating the server with the newest articles and researches!
    """

    def __init__(self):
        self._feeds = None  # the aggregator feeds that needs to be aggregated

    def aggregate(self):
        """
        Main function of the aggregator, it loops through all feeds, parses them and their entries, and updates
        the server!
        """
        self.update_feeds(debug=True)

        for feed_dict in self._feeds:
            feed = Feed(feed_dict)

            print(f'{feed}\n')

            for entry_data in feed.entries:
                entry = Entry(entry_data)
                entry.post()

    def update_feeds(self, debug=False):
        """
        Updates the aggregator feeds values!
        """
        if debug:
            self._feeds = data_django_feed
            return

        try:
            response = requests.get(FEED_URL)
            response.raise_for_status()
            self._feeds = response.json()
        except (HTTPError, ConnectionError) as e:
            # todo - handle different exception with different manner.
            print(e)


if __name__ == '__main__':
    aggr = Aggregator()

    aggr.aggregate()

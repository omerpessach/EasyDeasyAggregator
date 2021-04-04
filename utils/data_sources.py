from utils.consts import *


data_django_feed = [
    {
        URL: 'https://www.medicinenet.com/rss/general/digestion.xml',
        MISSING_FIELDS: '{0},{1},{2}'.format(MISSING_IMAGE, MISSING_SUMMARY, MISSING_WEBSITE),
        WEBSITE: 'medicinenet'
    },
    {
        URL: 'https://www.medicinenet.com/rss/general/diabetes.xml',
        MISSING_FIELDS: '{0},{1}'.format(MISSING_IMAGE, MISSING_SUMMARY),
        WEBSITE: 'medicinenet'
    },
]

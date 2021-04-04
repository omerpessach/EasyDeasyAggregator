

# region API endpoints

API_ROOT = 'http://127.0.0.1:8000/api/'
ARTICLES_URL = API_ROOT + 'articles/'
FEED_URL = API_ROOT + 'feeds/'

# endregion


# region prints

ARTICLE_DATA_PRINT = 'POSTing Data:\nTitle: {0}\nURL: {1}\nDate: {2}\nWebsite: {3}\nSummary: \n{4}\nTime to read: {5}\nDiseases: {6}\n'

SUCCESSFUL_POST_PRINT = 'Successfully POSTed'
ERROR_PRINT = 'There was an error POSTing'

# endregion


# region general

WORDS_PER_MINUTE = 120

# endregion

# region formats

DATE_FORMAT = "%Y-%m-%d"

# endregion


# region requests consts

MISSING_FIELDS = 'missing_fields'
WEBSITE = 'source_site'
TITLE = 'title'
URL = 'url'
SUMMARY = 'summary'
TIME_TO_READ = 'time_to_read'
PUBLISHED_DATE = 'published_date'
IMG = 'img'
SOURCE_SITE = 'source_site'
DISEASES = 'diseases'
ID = 'id'
NAME = 'name'

# endregion


# region missing fields types

MISSING_IMAGE = 'i'
MISSING_WEBSITE = 'w'
MISSING_SUMMARY = 's'

# endregion

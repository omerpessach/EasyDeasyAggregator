

# region API endpoints

API_ROOT = 'http://127.0.0.1:8000/api/'
ARTICLES_URL = API_ROOT + 'articles/'
FEED_URL = API_ROOT + 'feeds/'

# endregion


# region prints

ARTICLE_DATA_PRINT = 'POSTing data:\n{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n'
SUCCESSFUL_POST_PRINT = 'Successfully POSTed'
ERROR_PRINT = 'There was an error POSTing'

# endregion


# region general

WORDS_PER_MINUTE = 150

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
PUBLISHED_DATA = 'published_date'
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

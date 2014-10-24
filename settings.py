# settings.py

USE_DB = False
DB_HOST = 'localhost'
DB_PORT = 27017

# Twitter Settings
CONSUMER_KEY = 'your_consumer_key'
CONSUMER_SECRET = 'your_consumer_secret'
ACCESS_TOKEN = 'your_access_token'
ACCESS_TOKEN_SECRET = 'your_access_token_secret'

# Thresholds
EMAIL_THRESHOLD = 20
HASH_THRESHOLD = 45
DB_KEYWORDS_THRESHOLD = .55

# Time to Sleep for each site
SLEEP_SLEXY = 60
SLEEP_PASTEBIN = 30
SLEEP_PASTIE = 30

# Other configuration
tweet_history = "tweet.history"
log_file = "output.log"

PASTEBIN_URLS = ['pastebin.com', 
                 'http://www.hidebux.com/browse.php?u=sPdAUx2I0rbIyI9OSCeo1hSIoZYrooE%3D&b=0&f=norefer']

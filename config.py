# Production config
# Local config: instance/config.py (create one if not already available)
# Remove .example from this file's name after filling out all the keys

# Your own webhook verification token for Facebook to forward to
OWN_WEBHOOK_TOKEN='mfh'

# Do not allow debug mode for production
DEBUG=False

# Facebook Page Access Token
PAT = 'EAAEbZBmAst54BAKGzzdnbdPBLjerkEDkI40J2DF6RmptrD4OYSRnEGs99o1xFC4WNftIYfol1HWo1oRl0JHiyWG5ZBYJZBGOggZCPprHg8cwww12zZCywySJBVBPdg1JiPNwg3pc02jeZCehZCrpeZAsQrZCEj8HUepTClGRqLfoElQZDZD'
FACEBOOK_APP_ID = '312237146027934'
FACEBOOK_APP_SECRET = '284f9e356d2f06ce7d2fb30772d5c06a'

#Yelp
# v2
CONSUMER_KEY=""
CONSUMER_SECRET=""
TOKEN=""
TOKEN_SECRET=""

# v3
YELP_V3_TOKEN = 'IZU-CugRM1lHBGsGsrkCfz3549H5XaJZxvI0XY3ZjL67lMpyCidc2tstfblYwCYTELqmN6TXQWDEON6mVJ7GwDabRsKvNEhhauMLWm12-TtX3q-obI-AbQSHKXbSW3Yx'

# Heroku MongoDB ============
MONGO_URI = "mongodb://mauricio:mauricio1@ds161146.mlab.com:61146/mfhdatascience"
MONGO_DBNAME = 'mfhdatascience' # Get database

SIMSIMI_KEY = '9f389cfb-11e9-4a39-a02a-7eaac854eee1'

# Bot operation variables:
PRINT_INCOMING_PAYLOAD = False
PRINT_INCOMING_MESSAGE = False
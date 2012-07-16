from __builtin__ import frozenset

__author__ = 'Chris Bandy'

import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SECRET_KEY = 'testkey'
ADMINS = frozenset(["wiper"])

MONGO_HOST="localhost"
MONGO_PORT=27017
MONGO_USERNAME=""
MONGO_PASSWORD=""

FACEBOOK_KEY = ""
FACEBOOK_SECRET = ""
GOOGLE_KEY =""
GOOGLE_SECRET=""
TWITTER_KEY=""
TWITTER_SECRET=""


del os
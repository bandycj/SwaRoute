from __builtin__ import frozenset

__author__ = 'Chris Bandy'

import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SECRET_KEY = 'testkey'
ADMINS = frozenset(["wiper"])

MONGO_HOST="wiper-linux"
MONGO_PORT=27017
MONGO_USERNAME="swaroute"
MONGO_PASSWORD="4805fm3465"

del os
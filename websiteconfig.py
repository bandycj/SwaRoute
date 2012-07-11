from __builtin__ import frozenset

__author__ = 'Chris Bandy'

import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SECRET_KEY = 'testkey'
ADMINS = frozenset(["wiper"])
MONGODB_URL = 'mongodb://192.168.0.5/default'

del os
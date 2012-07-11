__author__ = 'Chris Bandy'

from datetime import datetime, timedelta
from functools import wraps
from flask import g, url_for, flash, abort, request, redirect

TIMEDELTA_UNITS = (
    ('year', 3600 * 24 * 365),
    ('month', 3600 * 24 * 30),
    ('week', 3600 * 24 * 7),
    ('day', 3600 * 24),
    ('hour', 3600),
    ('minute', 60),
    ('second', 1)
    )


def requires_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash(u'You need to be signed in for this page.')
            return redirect(url_for('general.login', next=request.path))
        return f(*args, **kwargs)

    return decorated_function


def requires_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.user.is_admin:
            abort(401)
        return f(*args, **kwargs)

    return requires_login(decorated_function)


def format_datetime(dt):
    return dt.strftime('%Y-%m-%d @ %H:%M')


def format_timedelta(delta, granularity='second', threshold=.85):
    if isinstance(delta, datetime):
        delta = datetime.utcnow() - delta
    if isinstance(delta, timedelta):
        seconds = int((delta.days * 86400) + delta.seconds)
    else:
        seconds = delta

    for unit, secs_per_unit in TIMEDELTA_UNITS:
        value = abs(seconds) / secs_per_unit
        if value >= threshold or unit == granularity:
            if unit == granularity and value > 0:
                value = max(1, value)
            value = int(round(value))
            rv = u'%s %s' % (value, unit)
            if value != 1:
                rv += u's'
            return rv
    return u''

def enum(**enums):
    return type('Enum', (object,), enums)
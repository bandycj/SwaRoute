from SwaRoute.swa_route.database import User
from flask import session
from flask.globals import request, current_app
from flask.helpers import flash, url_for
from flask_principal import identity_changed, Identity

__author__ = 'wiper'

def token_getter():
    return session.get('oauth_token')

def authorized(resp, method):
    next_url = request.args.get('next') or url_for('general.index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return False, next_url

    session['oauth_method'] = method
    return True, next_url

def post_authorization(token, oauth_id, method):
    u = User.objects.get_or_create(token=token, userid=oauth_id, method=method)
    session['oauth_id'] = oauth_id
    identity_changed.send(current_app._get_current_object(), identity=Identity(session['oauth_id']))
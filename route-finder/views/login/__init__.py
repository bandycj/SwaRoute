from __builtin__ import getattr
from exceptions import ImportError
import importlib
import os
import pkgutil
from flask import session
from flask.blueprints import Blueprint
from flask.globals import current_app, request
from flask.helpers import url_for, flash
from flask.wrappers import Response
from flaskext.oauth import OAuth
from flask_principal import identity_changed, AnonymousIdentity, Identity
from route_finder import login_manager
from route_finder.database import User
from werkzeug.utils import redirect

__author__ = 'Chris Bandy'
mod = Blueprint('login', __name__, url_prefix="/login")
oauth = OAuth()

[importlib.import_module(name) for _, name, _ in pkgutil.iter_modules([os.path.dirname(__file__)])]


@mod.route('/')
def login():
    return Response(
        'Select a login method.<br />' \
        '<a href="' + url_for('login.method', method="twitter") + '">twitter</a><br />' \
        '<a href="' + url_for('login.method', method="facebook") + '">facebook</a><br />' \
        '<a href="' + url_for('login.method', method="google") + '">google</a><br /><br />' \
        '<a href="' + url_for('general.index') + '">index</a><br /><br />'
    )

@mod.route('/<method>')
def method(method):
    try:
        package = "oauth_" + method
        auth_service = getattr(importlib.import_module("auth_service", package), "auth_service")
        return auth_service.authorize(callback=url_for('login.' + method + '_authorized', _external=True))
    except ImportError:
        flash("Unknown login method.")
        return redirect(url_for("login.login"))

@mod.route('/logout')
def logout():
    if 'oauth_method' in session:
        session.pop('oauth_method')
    if 'oauth_token' in session:
        session.pop('oauth_token')
    if 'oauth_resp' in session:
        session.pop('oauth_resp')
    if 'oauth_id' in session:
        session.pop('oauth_id')

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    return redirect(url_for("general.index"))

@login_manager.unauthorized_handler
def unauthorized():
    return Response('Please <a href="'+url_for("login.login")+'">Login</a>')

@login_manager.user_loader
def load_user(userid):
    return User.get(userid)

def token_getter():
    return session.get('oauth_token')

def authorized(resp, method):
    next_url = request.args.get('next') or url_for('general.index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return False, next_url

    session['oauth_method'] = method
    return True, next_url

def post_authorization(token, oauth_id):
    u = User.objects.get_or_create(token=token, userid=oauth_id)
    u.save()
    identity_changed.send(current_app._get_current_object(), identity=Identity(session['oauth_id']))
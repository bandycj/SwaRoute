from flask import session
from flask.blueprints import Blueprint
from flask.globals import current_app, request
from flask.helpers import url_for, flash
from flask.wrappers import Response
from flaskext.oauth import OAuth
from flask_principal import identity_changed, AnonymousIdentity, Identity
from swa_route import login_manager
from swa_route.database import User
from werkzeug.utils import redirect

__author__ = 'Chris Bandy'
mod = Blueprint('login', __name__, url_prefix="/login")
oauth = OAuth()


#[importlib.import_module(name) for _, name, _ in pkgutil.iter_modules([os.path.dirname(__file__)])]
import oauth_google as google
import oauth_facebook as facebook
import oauth_twitter as twitter
oauth_methods = (google, facebook, twitter)

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
    auth_service = None
    for oauth_method in oauth_methods:
        if method == oauth_method.method:
            auth_service = oauth_method.auth_service

    if auth_service is not None:
        return auth_service.authorize(callback=url_for('login.' + method + '_authorized', _external=True))
    else:
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

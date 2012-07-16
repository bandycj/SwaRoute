from flask import session
from flask.blueprints import Blueprint
from flask.globals import current_app
from flask.helpers import url_for, flash
from flask.wrappers import Response
from flask_login import logout_user
from flask_principal import AnonymousIdentity, identity_changed
from werkzeug.utils import redirect

__author__ = 'e83800'

class Login():
    app = None
    mod = Blueprint('login', __name__, url_prefix="/login")
    oauth_methods = None
    def __init__(self, app):
        self.app = app

        from .oauth_methods import Google, Facebook, Twitter
        google = Google(app.config['GOOGLE_KEY'], app.config['GOOGLE_SECRET'])
        facebook = Facebook(app.config['FACEBOOK_KEY'], app.config['FACEBOOK_SECRET'])
        twitter = Twitter(app.config['TWITTER_KEY'], app.config['TWITTER_SECRET'])
        self.oauth_methods = (google, facebook, twitter)

        self.mod.add_url_rule('/', 'index', self.login)
        self.mod.add_url_rule('/<method>', 'method', self.method)
        self.mod.add_url_rule('/logout', 'logout', self.logout)
        self.mod.add_url_rule('/google/authorized', 'google_authorized', google.authorized)
        self.mod.add_url_rule('/facebook/authorized', 'facebook_authorized', facebook.authorized)
        self.mod.add_url_rule('/twitter/authorized', 'twitter_authorized', twitter.authorized)

    def login(self):
        return Response(
            'Select a login method.<br />'\
            '<a href="' + url_for('login.method', method="twitter") + '">twitter</a><br />'\
                                                                      '<a href="' + url_for('login.method',
                method="facebook") + '">facebook</a><br />'\
                                     '<a href="' + url_for('login.method', method="google") + '">google</a><br /><br />'\
                                                                                              '<a href="' + url_for(
                'general.index') + '">index</a><br /><br />'
        )


    def method(self, method):
        auth_service = None
        for oauth_method in self.oauth_methods:
            if method == oauth_method.method:
                auth_service = oauth_method.auth_service

        if auth_service is not None:
            return auth_service.authorize(callback=url_for('login.' + method + '_authorized', _external=True))
        else:
            flash("Unknown login method.")
            return redirect(url_for("login.login"))


    def logout(self):
        if 'oauth_method' in session:
            session.pop('oauth_method')
        if 'oauth_token' in session:
            session.pop('oauth_token')
        if 'oauth_resp' in session:
            session.pop('oauth_resp')
        if 'oauth_id' in session:
            session.pop('oauth_id')

        logout_user()

        # Remove session keys set by Flask-Principal
        for key in ('identity.name', 'identity.auth_type'):
            session.pop(key, None)

        # Tell Flask-Principal the user is anonymous
        identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
        return redirect(url_for("general.index"))

    def get_blueprint(self):
        return self.mod
import urllib2
from SwaRoute.swa_route.database import User
from abc import ABCMeta, abstractmethod
from flaskext.oauth import OAuth
from flask import session
from flask.globals import request, current_app
from flask.helpers import json, flash, url_for
from flask_login import login_user
from flask_principal import Identity, identity_changed
from werkzeug.utils import redirect

__author__ = 'e83800'

class AbstractOauthMethod():
    __metaclass__ = ABCMeta
    method = ''

    def __init__(self, method, auth_service):
        self.method = method

        self.authorized = auth_service.authorized_handler(self.authorized)
        self._token_getter = auth_service.tokengetter(self.__token_getter)

    def authorized(self, resp):
        next_url = request.args.get('next') or url_for('general.index')
        if resp is None:
            flash(u'You denied the request to sign in.')
            return False, next_url

        session['oauth_method'] = self.method

        username = self.get_user_info(resp)

        u = User.objects(userid=username, method=self.method).first()
        if u == None:
            User(token=session['oauth_token'], userid=username, method=self.method).save()
        else:
            u.token = session['oauth_token'][0]
            u.save()
        login_user(u)

        session['oauth_id'] = username
        identity_changed.send(current_app._get_current_object(), identity=Identity(username))

        return redirect(next_url)

    @abstractmethod
    def get_user_info(self, resp):
        return NotImplementedError()

    def __token_getter(self):
        return session.get('oauth_token')

    def __unicode__(self):
        return self.method


class Facebook(AbstractOauthMethod):
    method = "facebook"
    auth_service = None

    def __init__(self, key, secret):
        self.auth_service = OAuth().remote_app(self.method,
            base_url='https://graph.facebook.com/',
            request_token_url=None,
            access_token_url='/oauth/access_token',
            authorize_url='https://www.facebook.com/dialog/oauth',
            consumer_key=key,
            consumer_secret=secret,
            request_token_params={'scope': 'email'}
        )
        super(Facebook, self).__init__(self.method, self.auth_service)

    def get_user_info(self, resp):
        session['oauth_token'] = (resp['access_token'], '')
        return self.auth_service.get('/me').data['name']


class Google(AbstractOauthMethod):
    method = "google"
    auth_service = None

    def __init__(self, key, secret):
        self.auth_service = OAuth().remote_app(self.method,
            base_url='https://www.googleapis.com/oauth2/v1/userinfo',
            authorize_url='https://accounts.google.com/o/oauth2/auth',
            request_token_url=None,
            request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email', 'response_type': 'code'},
            access_token_url='https://accounts.google.com/o/oauth2/token',
            access_token_method='POST',
            access_token_params={'grant_type': 'authorization_code'},
            consumer_key=key,
            consumer_secret=secret,
        )
        super(Google, self).__init__(self.method, self.auth_service)

    def get_user_info(self, resp):
        session['oauth_token'] = (resp['access_token'], '')
        url = self.auth_service.base_url + "?access_token=" + resp['access_token']
        userinfo = json.load(urllib2.urlopen(url))
        return userinfo['email']


class Twitter(AbstractOauthMethod):
    method = "twitter"
    auth_service = None

    def __init__(self, key, secret):
        self.auth_service = OAuth().remote_app(self.method,
            base_url='http://api.twitter.com/1/',
            request_token_url='http://api.twitter.com/oauth/request_token',
            access_token_url='http://api.twitter.com/oauth/access_token',
            authorize_url='http://api.twitter.com/oauth/authenticate',
            consumer_key=key,
            consumer_secret=secret
        )
        super(Twitter, self).__init__(self.method, self.auth_service)

    def get_user_info(self, resp):
        session['oauth_token'] = (resp['oauth_token'], resp['oauth_token_secret'])
        return resp['screen_name']
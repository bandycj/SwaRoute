import urllib2
from flask.helpers import json
from . import mod, oauth
from .login_utils import authorized, post_authorization, token_getter
from werkzeug.utils import redirect

__author__ = 'e83800'

method = "google"

auth_service = oauth.remote_app(method,
    base_url='https://www.googleapis.com/oauth2/v1/userinfo',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    request_token_url=None,
    request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email', 'response_type': 'code'},
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_method='POST',
    access_token_params={'grant_type': 'authorization_code'},
    consumer_key="690269901179.apps.googleusercontent.com",
    consumer_secret="pJFpkeuVPYhGWvrgifrp_TTB"
)

@mod.route('/' + method + '/authorized')
@auth_service.authorized_handler
def google_authorized(resp):
    authed, next_url = authorized(resp, method)

    if authorized:
        url = auth_service.base_url + "?access_token=" + resp['access_token']
        userinfo = json.load(urllib2.urlopen(url))
        post_authorization(resp['access_token'], userinfo['email'], method)

    return redirect(next_url)

@auth_service.tokengetter
def _token_getter():
    return token_getter()


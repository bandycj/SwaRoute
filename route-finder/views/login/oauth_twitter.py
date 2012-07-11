from route_finder.views.login import mod, oauth, post_authorization, authorized, token_getter
from werkzeug.utils import redirect

__author__ = 'e83800'

method = "twitter"
auth_service = oauth.remote_app(method,
    base_url='http://api.twitter.com/1/',
    request_token_url='http://api.twitter.com/oauth/request_token',
    access_token_url='http://api.twitter.com/oauth/access_token',
    authorize_url='http://api.twitter.com/oauth/authenticate',
    consumer_key='4hqvA1mfz3wceVLJcwX6Hg',
    consumer_secret='6T23FqDNvs0sVtnTt7flABP7f60QDXzZOjGqmrwy8'
)

@mod.route('/' + method + '/authorized')
@auth_service.authorized_handler
def twitter_authorized(resp):
    authed, next_url = authorized(resp, method)

    if authorized:
        post_authorization(resp['oauth_token'], resp['screen_name'])

    return redirect(next_url)

@auth_service.tokengetter
def _token_getter():
    return token_getter()
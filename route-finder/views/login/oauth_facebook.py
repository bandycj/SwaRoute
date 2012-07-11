from route_finder.views.login import mod, oauth, post_authorization, authorized, token_getter
from werkzeug.utils import redirect

__author__ = 'e83800'

method = "facebook"

auth_service = oauth.remote_app(method,
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key="263617160413768",
    consumer_secret="d9bbcf56c71d13e4e8b611f91e072bb7",
    request_token_params={'scope': 'email'}
)

@mod.route('/' + method + '/authorized')
@auth_service.authorized_handler
def facebook_authorized(resp):
    authed, next_url = authorized(resp, method)

    if authed:
        userinfo = auth_service.get('/me')
        post_authorization(resp['access_token'], userinfo.data['name'])

    return redirect(next_url)

@auth_service.tokengetter
def _token_getter():
    return token_getter()

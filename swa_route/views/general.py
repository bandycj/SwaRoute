from flask.wrappers import Response
from flask import Blueprint, url_for,\
    session
from flask_login import login_required, current_user
from werkzeug.utils import redirect

__author__ = 'Chris Bandy'

mod = Blueprint('general', __name__)

@mod.route('/')
@login_required
def index():
#    if not current_user.is_authenticated():
#        return redirect(url_for("login.login"))
#    else:
    return Response('Hello %s, signed in with %s. <a href="%s">Logout?</a>' % (
        session['oauth_id'], session['oauth_method'], url_for("login.logout")))
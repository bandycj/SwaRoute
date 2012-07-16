from flask.helpers import url_for
from flask.wrappers import Response
from flask_login import LoginManager
from flask_principal import RoleNeed, Permission, Principal

__author__ = 'Chris Bandy'

from flask import Flask, render_template
app = Flask(__name__)
app.config.from_object('websiteconfig')

from SwaRoute.swa_route import database
database.init_db(app)


login_manager = LoginManager()
login_manager.init_app(app)
#login_manager.login_view = "login"
#login_manager.login_message = u"Please log in to access this page."
#login_manager.refresh_view = "reauth"

principals = Principal(app)
user_permission = Permission(RoleNeed('user'))

from SwaRoute.swa_route import utils
from SwaRoute.swa_route.views import general
from SwaRoute.swa_route.views.login import Login
login = Login(app)
app.register_blueprint(login.get_blueprint())
app.register_blueprint(general.mod)

app.jinja_env.filters['datetimeformat'] = utils.format_datetime
app.jinja_env.filters['timedeltaformat'] = utils.format_timedelta

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@login_manager.unauthorized_handler
def unauthorized():
    return Response('Please <a href="' + url_for("login.index") + '">Login</a>')


@login_manager.user_loader
def load_user(userid):
    from SwaRoute.swa_route.database import User
    return User.objects(userid=userid).first()
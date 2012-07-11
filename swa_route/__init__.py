from flask_login import LoginManager
from flask_principal import RoleNeed, Permission, Principal

__author__ = 'Chris Bandy'

from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object('websiteconfig')

login_manager = LoginManager()
login_manager.init_app(app)

principals = Principal(app)
user_permission = Permission(RoleNeed('user'))

from SwaRoute.swa_route import utils
from SwaRoute.swa_route.views import general, login

app.register_blueprint(login.mod)
app.register_blueprint(general.mod)

app.jinja_env.filters['datetimeformat'] = utils.format_datetime
app.jinja_env.filters['timedeltaformat'] = utils.format_timedelta

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


from flask_wtf.form import Form
from wtforms import validators
from wtforms.fields.simple import TextField, PasswordField, HiddenField
from wtforms.fields.core import BooleanField
from route_finder import User
from route_finder.utils import enum

__author__ = 'e83800'

Errors = enum(
    UNKNOWN_USER="Unknown user.",
    INVALID_PASSWORD="Invalid password.",
    USERNAME_UNAVAILABLE="Username unavailable.",
    EMAIL_IN_USE="Email address in use.",
)


class LoginForm(Form):
    openid = TextField('OpenID URL:', [validators.Required()])
    next = HiddenField('next')

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.objects(openid=self.openid.data).first()
        if user is None:
            self.openid.errors = [Errors.UNKNOWN_USER]
            return False

        self.username = user
        return True

class FirstLoginForm(Form):
    username = TextField('Username', [validators.Required()])
    next = HiddenField('next')

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        print self.username.data
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.objects(username=self.username.data).first()
        if user != None:
            self.username.errors = [Errors.USERNAME_UNAVAILABLE]
            return False

        if oid == None and user == None:
            user = User(openid=self.openid.data, username=self.username.data)
            user.save()

        self.username = user
        return True

class ProfileForm(Form):
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password', [validators.Required()])
    email = TextField('Email', [validators.Required()])
    admin = BooleanField('Admin', default=False)

    user = None
    is_admin = False

    def __init__(self, user, *args, **kwargs):
        kwargs['csrf_enabled'] = False

        if isinstance(user, User):
            self.user = user
            self.username = user.username
            self.email = user.email
            self.admin = user.admin
        self.is_admin = is_admin
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        print self.username.data
        rv = Form.validate(self)
        if not rv:
            return False

        if self.username.data != user.username:
            user = User.objects(username=self.username.data).first()
            if user != None:
                self.username.errors = [Errors.USERNAME_UNAVAILABLE]
                return False

        if self.username.data != user.username:
            email = User.objects(email=self.email.data).first()
            if email != None:
                self.email.errors = [Errors.EMAIL_IN_USE]
                return False

        self.username = user
        self.email = email
        return True

    def is_admin_form(self):
        return self.is_admin
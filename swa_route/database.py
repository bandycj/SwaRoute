__author__ = 'Chris Bandy'

from flask_mongoengine import  Document
from mongoengine.connection import connect
from mongoengine.fields import StringField, ReferenceField, DateTimeField, IntField
from swa_route import app

model = connect('swa_route',
    host=app.config['MONGO_HOST'],
    port=app.config['MONGO_PORT'],
    username=app.config['MONGO_USERNAME'],
    password=app.config['MONGO_PASSWORD']
)


class User(Document):
    token = StringField(max_length=200, required=True, unique=True)
    userid = StringField(max_length=200, required=True, unique_with="method")
    method = StringField(max_length=200, required=True, unique_with="userid")

    @property
    def is_admin(self):
        return self.openid in app.config['ADMINS']

    def is_user(self):
        if self.userid:
            return True
        else:
            return False

    def is_authenticated(self):
        return self.is_user()

    def is_active(self):
        return self.is_user()

    def is_anonymous(self):
        return self.is_user()

    def get_id(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.userid


class Airport(Document):
    iataCode = StringField(max_length=3, required=True, primary_key=True)
    name = StringField(max_length=32, required=True)

    def __unicode__(self):
        return self.iataCode


class Flight(Document):
    origin = ReferenceField(Airport, required=True)
    destination = ReferenceField(Airport, required=True, unique_with='origin')
    flightNum = IntField(required=True, unique_with='origin')
    fromDate = DateTimeField(required=True, unique_with='origin')
    toDate = DateTimeField(required=True, unique_with='origin')
    ska = DateTimeField(required=True, unique_with='origin')
    skd = DateTimeField(required=True, unique_with='origin')

    def __unicode__(self):
        return self.origin['iataCode'] + self.destination['iataCode'] + str(self.flightNum) + str(fromDate) + str(
            toDate)

from mongoengine import *
connect('corps')
from datetime import datetime

class Agent(Document):
    host = StringField(required=True)
    created_at = DateTimeField(default=datetime.now())


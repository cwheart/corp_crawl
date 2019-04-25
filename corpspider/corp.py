from mongoengine import *
connect('corps')

class Corp(Document):
    meta = {'collection': 'corps'}

    no = StringField(required=True)
    name = StringField(required=False)
    legal_person = StringField(required=False)
    area = StringField(required=False)
    tp = StringField(required=False)
    address = StringField(required=False)
    corp_type = StringField(required=False)
    link = StringField(required=False)
    d101a = BooleanField(default=False)
    d101t = BooleanField(default=False)
    d110a = BooleanField(default=False)
    d110t = BooleanField(default=False)


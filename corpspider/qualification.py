from mongoengine import *
connect('corps')

class Qualification(Document):
    meta = {'collection': 'qualifications'}
    corp_no = StringField(required=True)
    name = StringField(required=False)
    no = StringField(required=False)
    tp = StringField(required=False)
    published_at = StringField(required=False)
    published_org = StringField(required=False)
    qua_type = StringField(required=False)
    expired_at = StringField(required=False)


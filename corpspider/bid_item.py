from mongoengine import *
connect('corps')

class BidItem(Document):
    corp_id = StringField(required=True)
    corp_no = StringField(required=True)
    published_at = StringField(required=False)
    title = StringField(required=False)
    customer = StringField(required=False)

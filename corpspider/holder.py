from mongoengine import *
connect('corps')

class HolderItem(EmbeddedDocument):
    corp_no = StringField(required=True)
    name = StringField(required=False)
    percent = StringField(required=False)
    paid_at = StringField(required=False)
    amount = StringField(required=False)
    tags = ListField(StringField(), default=list)
    extra = StringField(required=False)

class Holder(Document):
    corp_id = StringField(required=True)
    corp_no = StringField(required=True)
    hoder_count = StringField(required=False)
    items = ListField(EmbeddedDocumentField(HolderItem))

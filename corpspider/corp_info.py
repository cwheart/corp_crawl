from mongoengine import *
connect('corps')

class InfoItem(EmbeddedDocument):
    cate = StringField(required=True)
    name = StringField(required=False)
    count = StringField(required=False)

class CorpInfo(Document):
    corp_id = StringField(required=True)
    corp_no = StringField(required=True)
    counters = DictField()
    items = EmbeddedDocumentListField(InfoItem)

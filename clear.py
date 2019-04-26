# -*- coding: utf-8 -*-
from corpspider.corp import Corp
from datetime import datetime

pipeline = [
    { '$match': { 'deleted_at': None, 'link': { '$ne': None } } },
    { '$group': { '_id': "$link", 'count': { '$sum': 1 } } },
    { '$match': { 'count': { '$gt': 1 } } },
]

for corp in Corp.objects().aggregate(*pipeline):
    for blank_corp in Corp.objects(link=corp['_id'], legal_person=None):
        blank_corp['deleted_at'] = datetime.now()
        blank_corp.save()

# -*- coding: utf-8 -*-
from corpspider.corp import Corp
from corpspider.qualification import Qualification

for corp in Corp.objects(d101a=None, d101t=None, d110a=None, d110t=None):
    print 'update... ' + corp['name']
    if len(Qualification.objects(corp_no=corp['no'], name='建筑工程施工总承包一级')):
        corp['d101a'] = True
    if len(Qualification.objects(corp_no=corp['no'], name='建筑工程施工总承包特级')):
        corp['d101t'] = True
    if len(Qualification.objects(corp_no=corp['no'], name='市政公用工程施工总承包一级')):
        corp['d110a'] = True
    if len(Qualification.objects(corp_no=corp['no'], name='市政公用工程施工总承包特级')):
        corp['d110t'] = True
    corp.save()

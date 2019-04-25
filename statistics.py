# -*- coding: utf-8 -*-
from corpspider.corp import Corp
from corpspider.qualification import Qualification

for qualification in Qualification.objects(name='建筑工程施工总承包一级'):
    for corp in Corp.objects(no=qualification['corp_no']):
        print 'update' + corp['no']
        corp['d101a'] = True
        corp.save()
for qualification in Qualification.objects(name='建筑工程施工总承包特级'):
    for corp in Corp.objects(no=qualification['corp_no']):
        print 'update' + corp['no']
        corp['d101t'] = True
        corp.save()
for qualification in Qualification.objects(name='市政公用工程施工总承包一级'):
    for corp in Corp.objects(no=qualification['corp_no']):
        print 'update' + corp['no']
        corp['d110a'] = True
        corp.save()
for qualification in Qualification.objects(name='市政公用工程施工总承包特级'):
    for corp in Corp.objects(no=qualification['corp_no']):
        print 'update' + corp['no']
        corp['d110t'] = True
        corp.save()





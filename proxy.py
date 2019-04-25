# -*- coding: utf-8 -*-
from corpspider.agent import Agent
from datetime import datetime
import time
import requests

while True:
    url = 'http://dps.kdlapi.com/api/getdps/?orderid=995609298222197&num=1&pt=1&sep=1'
    count = 3
    for i in range(0, count):
        agent = Agent(host=requests.get(url).text)
        agent.save()
    print "sleep...."
    print datetime.now()
    time.sleep(30 * 60)

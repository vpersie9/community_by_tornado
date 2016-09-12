#-*-coding:utf-8-*-
__author__ = 'vpersie9'

import random
from settings import PROXIES
class RandomUserAgent(object):
    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(self.agents))

class ProxyMiddleware(object):
    def process_request(self, request, spider):
        proxy = random.choice(PROXIES)
        print "**************ProxyMiddleware no pass************" + proxy
        request.meta['proxy'] = proxy
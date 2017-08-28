#coding:utf-8

import urllib2
import re
import urlparse
import datetime
import time

def download(url,user_agent='wswp',proxy=None,num_retries=2):
    '''
    下载页面
    :param url:
    :param user_agent:
    :param num_retries:
    :return:
    '''
    print 'downloading:',url

    headers = {'User-agent':user_agent}
    rq = urllib2.Request(url,headers=headers)

    opener = urllib2.build_opener()
    if proxy:
        proxy_params = {urlparse.urlparse(url).scheme:proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))
    try:
        # html = urllib2.urlopen(rq).read()
        html = opener.open(rq).read()
    except urllib2.URLError as e:
        print 'Download err:',e.reason
        html = None

        #当服务器返回5XX时，表示服务器有问题，这个时候可以再重新试一次
        if num_retries>0:
            if hasattr(e,'code') and 500<=e.code<600:
                return download(url,num_retries-1)

    return html



class Throttle:
    def __init__(self,delay):
        self.delay = delay
        self.domain = {}


    def wait(self,url):
        domain = urlparse.urlparse(url).netloc
        last_accessed = self.domain.get(domain)
        if last_accessed is not None and self.delay>0:
            sleep_secs = self.delay - (datetime.datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                print 'sleep now '
                time.sleep(3)
        self.domain[domain] = datetime.datetime.now()

# html = download('http://example.webscraping.com/')
th = Throttle(5)
for i in range(2):
    th.wait('http://example.webscraping.com/sitemap.xml')
    html = download('http://example.webscraping.com/sitemap.xml')
    links = re.findall('<a href="(.*?)">',html)
    for link in links:
        print link

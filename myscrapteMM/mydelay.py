# -*- coding: utf-8 -*-
__author__ = "langtuteng" 
import time
import urlparse
import datetime

class Delay(object):
    '''
    延缓爬虫的下载速度
    '''

    def __init__(self,delay_time):
        '''

        :param delay_time:
        :param demain:
        '''
        self.delay_time = delay_time
        self.domains = {}


    def wait(self,url):
        '''
        睡眠时间
        :param url:
        :return:
        '''
        domain = urlparse.urlparse(url).netloc
        last_access_time = self.domains.get(domain)
        if last_access_time is not None and self.delay_time>0:
            sleep_secs = self.delay_time - (datetime.datetime.now() - last_access_time).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)

        #update the last_access_time
        self.domains[domain] = datetime.datetime.now()


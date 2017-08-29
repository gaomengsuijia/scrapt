#coding:utf-8

import urllib2
from mycache import Disk_cache
from lxml import etree
import os,sys
from mydelay import Delay


DEFAULT_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

class Download(object):
    '''
    下载html
    '''
    def __init__(self,url,num_retries=None,user_head=DEFAULT_AGENT,cache=None,delay_time = 3):
        self.url = url
        self.num_retries = num_retries
        self.user_head = user_head
        self.cache = cache
        self.delay = Delay(delay_time)



    def __call__(self,url):
        '''
        ，检查缓存时否可用
        :param url:
        :return:
        '''
        result = None
        if self.cache:
            try:
                print url
                result = self.cache[url]
            except KeyError as e:
                pass
            else:
                if self.num_retries > 0 and 500<=result['code']<600:
                    result = None

        if result == None:
            self.delay.wait(url)
            result = self.myload()['html']
            print result
            #将结果保存到缓存中
            self.cache[url] = result
            print result

        return result


    def myload(self,data=None):
        '''
        下载html
        :return:
        '''
        print 'loading %s'%self.url
        req = urllib2.Request(self.url,data,self.user_head)
        try:
            response = urllib2.urlopen(req)
            html = response.read()
            code = response.code
        except urllib2.URLError as e:
            print 'download erro',e.reason
            html = ''
            if self.num_retries > 0:
                if hasattr(e,'code'):
                    code = e.code
                    if 500<e.code<600:
                        self.myload()
            else:
                code = None

        return {'html':html,'code':code}





if __name__ == "__main__":
    cache_dir = BASE_DIR + '\cache\\'
    print cache_dir
    mydisk_cache = Disk_cache(cache_dir)
    mydown = Download('http://jandan.net/ooxx',cache=mydisk_cache)
    ht = mydown.myload()
    links = mydown.get_links(ht)

    for link in links:
        mydown.save_img(link)
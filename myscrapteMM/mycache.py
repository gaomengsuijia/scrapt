#coding:utf-8
import urlparse
import os,sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# print BASE_DIR
import re
try:
    import cPickle as pickle
except ImportError:
    import pickle
import zlib
# from mydownload import Download

import datetime

class Disk_cache(object):
    '''

    disk cache
    '''

    def __init__(self,cache_dir,expired = datetime.timedelta(days=30),compress = False):
        self.cache_dir = cache_dir
        self.expired = expired
        self.compress = compress


    def __getitem__(self, url):
        '''
        get url
        :param url:
        :return:
        '''
        file_path = self.url_to_path(url)
        if os.path.exists(file_path):
            try:
                f  = open(file_path,'rb')
                data = f.read()
            except OSError:
                raise OSError(file_path + 'can not open file')

            if self.compress:
                data = zlib.decompress(data)
            html, expired_time = pickle.loads(data)
            if self.hasexpired(expired_time):
                raise KeyError(url + ' has expired')

        else:
            raise OSError(file_path + 'not find')


        return html



    def __setitem__(self, url, result):
        '''
        set url
        :param url:
        :param result:
        :return:
        '''
        file_path = self.url_to_path(url)
        folder = os.path.dirname(file_path)
        if not os.path.exists(folder):
            os.mkdir(folder)

        data = pickle.dumps((result,datetime.datetime.utcnow()))

        if self.compress:
            data = zlib.compress(data)

        try:
            with open(file_path,'wb') as f:
                f.write(data)
        except OSError:
            print 'can not open file'



    def url_to_path(self,url):
        '''
        url to path
        :return:
        '''
        url_parse = urlparse.urlsplit(url)
        path = url_parse.path
        if urlparse:
            if not path:
                path = '/index.html'
            if path.endswith('/'):
                path = '/index.html'

            file_path = url_parse.netloc + path + url_parse.query
            #替换文件系统不支持的字符
            file_path = re.sub('[^/0-9a-zA-Z\-.,;_ ]', '_', file_path)
            #截取最多255个字符，以保证文件系统支持
            file_path = '/'.join(segment[:255] for segment in file_path.split('/'))
            file_path = file_path.replace('/','\\')
            return os.path.join(self.cache_dir, file_path)


    def hasexpired(self,timestap):
        '''
        判断是否过期
        :param timestap:
        :return:
        '''

        if datetime.datetime.utcnow() > timestap + self.expired:
            return True

        else:
            return False







if __name__ == "__main__":

    cache_dir = BASE_DIR + '\cache\\'
    print cache_dir
    mydisk_cache = Disk_cache(cache_dir)
    url = 'http://www.baidu.com/index'
    mydown = Download('http://www.baidu.com')
    html = mydown.myload()

    # mydisk_cache[url]
    # mydisk_cache[url] = html
    print mydisk_cache[url]
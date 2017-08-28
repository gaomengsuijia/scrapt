#coding:utf-8

import urllib2
from mycache import Disk_cache
from lxml import etree
import os,sys
class Download(object):
    '''
    下载html
    '''
    def __init__(self,url):
        self.url = url


    def myload(self):
        html = urllib2.urlopen(self.url).read()
        return html


    def get_links(self,html_content):
        '''
        获取url
        :return:
        '''
        links = etree.HTML(html_content).xpath('//ol[@class="commentlist"]/li/div/div/div[2]/p/img/@src')
        return links

    def save_img(self,img_link):
        '''
        保存图片
        :return:
        '''
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        img_name = img_link.split('/')[-1]
        file_foder = BASE_DIR + '/images/'
        if not os.path.exists(file_foder):
            os.mkdir(file_foder)

        file_path = file_foder + img_name
        try:
            img_link = 'http:' + img_link
            img_stream = urllib2.urlopen(img_link).read()
        except BaseException:
            raise BaseException(img_link + 'fail load')

        try:
            with open(file_path,'wb') as f:
                f.write(img_stream)
                print '%s loading sucess'%img_link

        except OSError:
            raise OSError(file_path +'file not creat')








if __name__ == "__main__":

    mydown = Download('http://jandan.net/ooxx')
    ht = mydown.myload()
    links = mydown.get_links(ht)

    for link in links:
        mydown.save_img(link)
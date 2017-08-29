#coding:utf-8
from lxml import etree
import os
import urllib2
from mydownload import Download
import re
import robotparser
import urlparse
import mycache
from mydelay import Delay
import itertools

DEFAULT_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}


def link_crawler(seed_url,link_re,max_depth=2):
    '''
    主运行函数
    :return:
    '''
    urls = [seed_url]
    # urls_tp = set(urls)
    urls_dict = {seed_url:0}
    num_urls = 0
    rp = get_robots(seed_url)
    ht = Download(seed_url)

    while urls:
        url = urls.pop()
        depth = urls_dict[url]
        if rp.can_fetch(DEFAULT_AGENT,url):
            links = get_links(ht)
            for link in links:
                if re.match(seed_url, link_re):
                    link = urlparse.urljoin(seed_url, link)
                    if link not in urls_dict:
                        urls_dict[link] = depth + 1
                        urls.append(link)

            num_urls += 1
            if num_urls > max_depth:
                break
        else:
            print 'not download'




def get_robots(url):
    '''
    获取网站的robots.txt
    :param url:
    :return:
    '''
    rp = robotparser.RobotFileParser(url)
    rp.set_url(urlparse.urljoin(url + 'robots.txt'))
    rp.read()
    return rp



def get_links(ht):

    '''
    获取url
    :return:
    '''
    links = etree.HTML(ht).xpath('//ol[@class="commentlist"]/li/div/div/div[2]/p/img/@src')
    return links


def save_img(img_link):
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
        with open(file_path, 'wb') as f:
            f.write(img_stream)
            print '%s loading sucess' % img_link

    except OSError:
        raise OSError(file_path + 'file not creat')

def get_maxpn(url,cache):
    '''
    得到pagenuber最大数
    :param url:
    :return:
    '''
    ht = Download(url,cache=cache)(url)
    pagenumber = etree.HTML(ht).xpath('//*[@id="comments"]/div[3]/div/span')[0].text
    return pagenumber



if __name__ == "__main__":
    cache_dir = mycache.BASE_DIR + '\cache\\'
    cache = mycache.Disk_cache(cache_dir)
    url = 'http://jandan.net/ooxx/'
    pagenumber = int(get_maxpn(url,cache).rstrip(']').lstrip('['))
    print pagenumber
    ht = Download(url, cache=cache)
    while pagenumber>0:
        url_page = '%spage-%s#comments'%(url,str(pagenumber))
        ht(url_page)
        pagenumber -= 1


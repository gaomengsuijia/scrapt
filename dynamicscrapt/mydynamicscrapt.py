# -*- coding: utf-8 -*-
__author__ = "langtuteng" 
import json
from mydownload import  Download
import urllib2
import csv




def dynamic_scrapt(url):
    return urllib2.urlopen(url).read()



if __name__ == "__main__":

    zimu_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q'
            ,'r','s','t','u','v','w','x','y','z']

    # url = 'http://example.webscraping.com/places/ajax/search.json?&search_term=a&page_size=10&page=0'
    # dynamic_scrapt(url)
    # ht = Download()(url)
    # html = ['html']
    # countrys = set()
    FIELDS = ['id','country','pretty_link']
    wr = csv.writer(open('country.csv','w'))
    wr.writerow(FIELDS)

    for word in zimu_list:
        page = 0
        while True:
            link = 'http://example.webscraping.com/places/ajax/search.json?&search_term=%s&page_size=10&page=%s'%(word,str(page))
            html = dynamic_scrapt(link)
            strs = json.loads(html, encoding="utf-8")
            for each_list in strs['records']:
                # wr.writerow([each_list['id'],each_list['country'],each_list['pretty_link']])
                rows = [each_list[field] for field in FIELDS]
                wr.writerow(rows)
            page += 1
            if page>strs['num_pages']:
                break




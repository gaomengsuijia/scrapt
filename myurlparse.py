# -*- coding: utf-8 -*-
__author__ = "langtuteng" 

import urlparse


url = "http://www.baidu.com/nihao/goushi/?a=0&b=3"
url1 = "http://jandan.net/ooxx/page-4#comments"

print urlparse.urlparse(url)
print urlparse.urlsplit(url)
print urlparse.urlparse(url1)
print urlparse.urlsplit(url1)
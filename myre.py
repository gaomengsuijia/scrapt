import re

url = 'http://example.webscrapting.com/defualt/view/a--1'
url1 = 'cdeabc'
url_pattn1 = '[^/0-9a-zA-Z\-.,;_]'
url_pattn2 = 'abc'
url_re = re.sub(url_pattn2,'_',url)
url_ma = re.match(url_pattn2,url1)
if url_ma:
    print url_ma.group(0)
else:
    print 'no match'
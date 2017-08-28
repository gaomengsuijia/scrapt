import csv
import re
import lxml
class ScrapeCallback:
    def __init__(self):
        self.write = csv.writer(open('countries.csv','w'))
        self.fields = ('area','population','ios')
        self.write.writerow(self.fields)


    def __call__(self, url, html):
        if re.search('/views/',url):
            tree = lxml.html.fromstring(html)
            row = []
            for field in self.fields:
                row.append(tree.cssselect('table > tr#places_{}_row) > td.w2p_fw'.format(field))[0].text_content())
                self.write.writerow(row)
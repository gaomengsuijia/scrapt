#coding:utf-8

import csv

info = [1,2,3,4,5,6]

myList=[[1,2,3],[4,5,6]]

with open('my.csv','wb') as f:
    mywrite = csv.writer(f)
    mywrite.writerow(info)
    mywrite.writerow(myList)
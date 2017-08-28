#coding:utf-8

class Person(object):
    def __init__(self,name):
        self.name = name


    def __call__(self):
        try:
            print 'wo shi call 方法出来的'
            print self.name

        except BaseException as e:
            print 'erro:%s'%str(e)



    def pr(self):
        print self.name

xiaotu = Person('xiaotu')
xiaotu.pr()
xiaotu()
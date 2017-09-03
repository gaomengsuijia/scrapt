# -*- coding: utf-8 -*-
__author__ = "langtuteng"
from pymongo import MongoClient
from datetime import datetime,timedelta
try:
    import cPickle as pickle
except ImportError:
    import pickle

import zlib
from bson.binary import Binary
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Mogocache(object):
    '''
    mogocache
    '''

    def __init__(self,client=None,expires=timedelta(days=30)):
        self.client = MongoClient('localhost', 27017) if client is None else client
        self.db = self.client.cache
        self.db.webpage.create_index('timestamp', expireAfterSeconds=expires.total_seconds())

    def __contains__(self, url):
        try:
            self[url]
        except KeyError:
            return False
        else:
            return True


    def __getitem__(self, url):
        record = self.db.webpage.find_one({'__id':url})
        if record:
            pickle.loads(zlib.decompress(record['result']))
        else:
            raise KeyError('the key %s is not find'%url)


    def __setitem__(self, url, result):
        '''
        存储数据，Binary是mongo的专用格式，必须这么转化才能存储
        :param url:
        :param result:
        :return:
        '''
        record = {'result': Binary(zlib.compress(pickle.dumps(result))), 'timestamp': datetime.utcnow()}
        self.db.webpage.update({'_id': url}, {'$set': record}, upsert=True)


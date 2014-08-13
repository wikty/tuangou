# -*- coding: UTF-8 –*-
import re
import json

import tornado.web
import sqlite3dbm

from cfg import DATA_FILE
from utils import content_rank


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.tmpl')

class KeywordsHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.db = sqlite3dbm.sshelve.open(DATA_FILE)
    def on_finish(self):
        self.db.close()
    def get(self):
        term = self.get_argument('term', None)
        keywords = re.compile(r'\s+').split(term)
        content = [kw for city in self.db.itervalues() for kw in city.get('keywords', [])]
        result = content_rank(content, *keywords)
        self.write(json.dumps(result))

class QueryHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.db = sqlite3dbm.sshelve.open(DATA_FILE)
    def on_finish(self):
        self.db.close()
    def get(self):
        item = self.get_argument('item', None)
        keywords = re.compile(r'\s+').split(item)
        content = [deal for city in self.db.itervalues() 
                            for k, site in city.iteritems()
                                if k != 'keywords'
                                    for deal in site['deals'].itervalues()]
        result = content_rank(content, *keywords, keys=['deal_title'])
        
        self.render('result.tmpl', deals=result)


# import os
# from cfg import STATIC_DIR
#class StaticHandler(tornado.web.RequestHandler):
#   def get(self, filename):
#       if filename:
#           filename = os.path.join(STATIC_DIR, filename)
#           if not os.path.isfile(filename):
#               return
#           with open(filename, 'r') as f:
#               content = f.read()
#           file_type = filename[filename.rfind('.'):]
#           if file_type == '.js':
#               content_type = 'application/x-javascript'
#           elif file_type == '.css':
#               content_type = 'text/css'
#           else:
#               content_type = 'text/html'
#           self.set_header('Content-Length', len(content))
#           self.set_header('Content-Type', content_type)
#           self.write(content)

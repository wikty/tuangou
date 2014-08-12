import tornado.web

from tornado.web import URLSpec

from cfg import SETTINGS
from views import IndexHandler, KeywordsHandler, QueryHandler

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
		    URLSpec(r'/', IndexHandler, name='index_url'),
		    URLSpec(r'/keywords', KeywordsHandler, name='keywords_url'),
		    URLSpec(r'/query', QueryHandler, name='query_url')
		]
		tornado.web.Application.__init__(self, handlers, **SETTINGS)

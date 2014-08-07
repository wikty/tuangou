import tornado.web.Application

from cfg import TMPL_DEFAULT_VARS
from views import IndexHandler, KeywordsHandler, QueryHandler, StaticHandler

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(TMPL_DEFAULT_VARS['index_url'], IndexHandler),
			(TMPL_DEFAULT_VARS['keywords_url'], KeywordsHandler),
			(TMPL_DEFAULT_VARS['query_url'], QueryHandler),
			(TMPL_DEFAULT_VARS['static_url']+r'/(.*)', StaticHandler)
		]
		settings = dict()
		tornado.web.Application.__init__(self, handlers, settings)
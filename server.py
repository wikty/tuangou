import tornado.options
import tornado.ioloop
import tornado.httpserver

from app import Application

def run():
	tornado.options.parse_command_line()  # get the defined port
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(tornado.options.options.port)
	print("Server is listening on port %d ...." % tornado.options.options.port)
	tornado.ioloop.IOLoop.instance().start()

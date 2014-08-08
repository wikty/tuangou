# -*- coding: UTF-8 –*-
import os
import re
import json
import shelve

import xml.etree.ElementTree as ET

import tornado.web.RequestHandler

from cfg import STATIC_DIR, DATA_DIR, DATA_FILE
from utils import render_template, content_rank


class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		content = render_template('index.tmpl')
		self.write(content)

class KeywordsHandler(tornado.web.RequestHandler):
	def initialize(self):
		self.db = shelve.open(DATA_FILE)
	def on_finish(self):
		self.db.close()
	def get(self):
		term = self.get_argument('term', None)
		keywords = re.compile(r'\s+').split(term)
		content = self.db['keywords']
		result = content_rank(content, *keywords)
		self.write(json.dumps(result))

class QueryHandler(tornado.web.RequestHandler):
	def get(self):
		item = self.get_argument('item', None)
		
		nofound = True
		mystr = u''
		# mystr = u'<div class="ui-widget"><form action="/query" method="get">
		# <input type="text" name="item" class="span3" id="search" value="'+k+u'" />
		# <input type="submit" name="submit" value="团Go" class="btn btn-primary" />
		# </form></div>'
		for subdir in os.listdir(DATA_DIR):
			subdir = os.path.join(DATA_DIR, subdir)
			if os.path.isdir(subdir):
				for filename in os.listdir(subdir):
					filename = os.path.join(subdir, filename)
					if not os.path.isfile(filename):
						print(filename)
						continue
					tree = ET.parse(filename)
					root_node = tree.getroot()
					i = -1
					mystr += u'<ul class="thumbnails row-fluid"><div class="row-fluid">'
					for data_node in root_node.iter('data'):
						deal_node = data_node.find('deal')
						deal_name = deal_node.find('deal_name').text
						deal_title = deal_node.find('deal_title').text
						if item in deal_name or item in deal_title:
							i += 1
							deal_url = deal_node.find('deal_url').text
							deal_img = deal_node.find('deal_img').text
							deal_desc = deal_node.find('deal_desc').text
							start_time = deal_node.find('start_time').text
							end_time = deal_node.find('end_time').text
							timestr = u'开始：'+time.strftime('%Y-%m-%d %H:%M:%S',
							time.localtime(int(start_time)))
							timestr += u'<br/>结束：'+time.strftime('%Y-%m-%d %H:%M:%S',
							time.localtime(int(end_time)))
							
							if i%4==0 and i!=0:
								mystr +=u'</div><hr/><div class="row-fluid">'
							mystr += u'<li class="span3"><div class="thumbnail">'
							mystr += u'<a href="'+deal_url+'"><img src="'+deal_img+u'" /></a>'
							mystr += u'<h4 class="media-heading">'+deal_title+u'</h4>'
							mystr += u'<p class="muted">'+timestr+u'</p>'
							mystr += u'<p>'+deal_desc+u'</p>'
							mystr += u'<p><a href="'+deal_url+u'" class="btn">了解更多</a></p>'
							mystr += u'</div></li>'
							nofound = False
		if nofound:
			mystr += u'<h3>对不起！没有找到您想要的结果</h3>'
		mystr += u'</div></ul>'
		mystr += u'<script type="text/javascript">document.getElementById("search").value="'+k+u'"</script>'
		self.write(mystr)

class StaticHandler(tornado.web.RequestHandler):
	def get(self, filename):
		if filename:
			filename = os.path.join(STATIC_DIR, filename)
			if not os.path.isfile(filename):
				return
			with open(filename, 'r') as f:
				content = f.read()
			file_type = filename[filename.rfind('.'):]
			if file_type == '.js':
				content_type = 'application/x-javascript'
			elif file_type == '.css':
				content_type = 'text/css'
			else:
				content_type = 'text/html'
			self.set_header('Content-Length', len(content))
			self.set_header('Content-Type', content_type)
			self.write(content)
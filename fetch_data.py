import os
import shelve

from contextlib import closing
from xml.etree.ElementTree import fromstring

import tornado.httpclient

from cfg import DATA_DIR, DATA_FILE, SITES, CITYS

def fetch(url, city, site):
	reserved_fields = [
		'deal_id',
		'deal_title',
		'deal_name',
		'deal_url',
		'deal_img',
		'value',
		'price',
		'rebate',
		'start_time',
		'end_time',
	]
	http_header = {'User-Agent': 'Chrome'}
	http_request = tornado.httpclient.HTTPRequest(
		url=url, 
		method='GET', 
		headers=http_header, 
		connect_timeout=20, 
		request_timeout=600
	)
	http_client = tornado.httpclient.HTTPClient()
	print("Download [%s] data from [%s] ..." % (city, site))
	http_response = http_client.fetch(http_request)
	print("Downloading Is Finished")
	print('')
	print('Parsing Data...')
	with closing(shelve.open(DATA_FILE)) as s:
		if s['keywords'] is None:
			s['keywords'] = []
		root_node = fromstring(http_response.body)
		for deal_node in root_node.iterfind('deal'):
			deal_id = deal_node.find('deal_id')
			for node in deal_node:
				if node.tag in reserved_fields:
					if node.tag == 'deal_title' or node.tag == 'deal_name':
						s['keywords'].append(node.text)
					s[city][site]['deals'][deal_id][node.tag] = node.text
	print('Parsing Is Finished')

if __name__ == "__main__":
	for city in CITYS:
		for site, url in SITES.items():
			fetch(url.format(city=city), city, site)

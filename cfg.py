# -*- coding: UTF-8 –*-
import os
import re
import sys

CITYS = ['hangzhou',]
SITES = {
	'meituan': 'http://www.meituan.com/api/v2/{city}/deals',
	# '55tuan': 'http://www.55tuan.com/partner/partnerApi?partner=wowo&{city}',
}

APP_ROOT = os.path.dirname(__file__)
STATIC_DIR = os.path.join(APP_ROOT, 'static')
TMPL_DIR = os.path.join(APP_ROOT, 'tmpl')
DATA_DIR = os.path.join(APP_ROOT, 'data')
DATA_FILE = os.path.join(DATA_DIR, 'data.db')

TMPL_404_PAGE = '404.tmpl'
TMPL_INC_TAG = re.compile(
	r'{%\s*include\s+(?P<quote>["\']?)(?P<filename>[-a-zA-Z0-9.]+)(?P=quote)\s*%}'
)

TMPL_VAR_TAG = re.compile(
	r'{{\s*(?P<varname>[a-zA-Z_][a-zA-Z0-9]*)\s*}}'
)

TMPL_DEFAULT_VARS = {
	'index_url': '/',
	'keywords_url': '/keywords',
	'query_url': '/query'
	'static_url': '/static',
	'site_name': u'团购搜'
}

SYS_ENCODING = 'utf-8'


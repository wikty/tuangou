# -*- coding: UTF-8 –*-
import os
import re
import sys

CITYS = ['lanzhou',]
SITES = {
	'meituan': 'http://www.meituan.com/api/v2/{city}/deals',
	# '55tuan': 'http://www.55tuan.com/partner/partnerApi?partner=wowo&{city}',
}

SYS_ENCODING = 'utf-8'

APP_ROOT = os.path.dirname(__file__)
STATIC_DIR = os.path.join(APP_ROOT, 'static')
TMPL_DIR = os.path.join(APP_ROOT, 'tmpl')
DATA_DIR = os.path.join(APP_ROOT, 'data')
DATA_FILE = os.path.join(DATA_DIR, 'data.db')

TMPL_DEFAULT_VARS = {
	'index_url': '/',
	'keywords_url': '/keywords',
	'query_url': '/query',
	'static_url': '/static',
	'site_name': u'团购搜'
}

TMPL_404_PAGE = '404.tmpl'

TMPL_INC_TAG = re.compile(r'''
	{%\s*								# delimiter
		include\s+						# include keyword
		(?P<quote>["']?)				# filename may be wrapped by quote
		(?P<filename>[-_~./\\\d\w\s]+)	# filename(the included file)
		(?P=quote)						# quote match pairs
	\s*%}								# delimiter
''', re.VERBOSE)

TMPL_VAR_TAG = re.compile(r'''
	{{\s*									# delimiter
		(?P<varname>[_\w][\w\d]*)			# variable name
		(
			\.(?P<dotkey>[_\w][\w\d]*)
			|
			\[(?P<quote>["'])(?P<barcketkey>[_\w][\w\d]*)(?P=quote)\]
		)?
	\s*}}									# delimiter
''', re.VERBOSE)

TMPL_IF_TAG = re.compile(r'''
	(?P<if>							# not support nest if, elif, else
		{%\s*if\s+(?P<ifvarname>[_\w][\w\d]*)\s*%}
	)
	(?P<ifcontent>.*)
	(?P<endif>
		{%\s*endif\s*%}
	)
''', re.VERBOSE | re.DOTALL)

TMPL_FOR_TAG = re.compile(r'''
	(?P<for>						# not support for nest
		{%\s*
		for\s+
		(?P<item>[_\w][\w\d]*)\s+
		in\s+
		(?P<items>[_\w][\w\d]*)
		\s*%}
	)
	(?P<forcontent>.*)
	(?P<endfor>
		{%\s*endfor\s*%}
	)
''', re.VERBOSE | re.DOTALL)
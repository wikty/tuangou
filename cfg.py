# -*- coding: UTF-8 -*-
import os
import sys


APP_ROOT = os.path.dirname(__file__)
STATIC_DIR = os.path.join(APP_ROOT, 'public')
TMPL_DIR = os.path.join(APP_ROOT, 'tmpl')
DATA_DIR = os.path.join(APP_ROOT, 'data')
DATA_FILE = os.path.join(DATA_DIR, 'data.db')

TMPL_404_PAGE = '404.tmpl'

SYS_ENCODING = 'utf-8'

SETTINGS = {
    'template_path': TMPL_DIR,
    'static_path': STATIC_DIR,
    'static_url_prefix': '/public/',
    'debug': True,
    'gzip': True,
	'site_name': u'团购搜',
	'author': 'XiaoWenBin'
}

CITYS = ['lanzhou',]
SITES = {
	'meituan': 'http://www.meituan.com/api/v2/{city}/deals',
	# '55tuan': 'http://www.55tuan.com/partner/partnerApi?partner=wowo&{city}',
}

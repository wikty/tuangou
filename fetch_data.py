import os

from contextlib import closing
from xml.etree.ElementTree import fromstring

import sqlite3dbm
import tornado.httpclient

# Heroku charge for clock, so drop this function
#from apscheduler.schedulers.blocking import BlockingScheduler

from cfg import DATA_FILE, SITES, CITYS

#sched = BlockingScheduler()


#@sched.scheduled_job('cron', day_of_week='0-6', hour='3-5')
def fetch_data():
    for city in CITYS:
        for site, url in SITES.items():
            fetch(url.format(city=city), city, site)

#sched.start()

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
    with closing(sqlite3dbm.sshelve.open(DATA_FILE, writeback=True)) as s:
        if not s.has_key(city):
            s[city] = {'keywords': []}
        deals_node = fromstring(http_response.body).find('deals')
        
        for data_node in deals_node.iterfind('data'):
            deal_node = data_node.find('deal')
            # shops_node = data_node.find('shops')
            deal_id = deal_node.find('deal_id').text
            for node in deal_node:
                if node.tag in reserved_fields:
                    if node.tag == 'deal_title' or node.tag == 'deal_name':
                        s[city]['keywords'].append(node.text)
                    if not s[city].has_key(site):
                        s[city][site] = {'deals': {}}
                    if not s[city][site]['deals'].has_key(deal_id):
                        s[city][site]['deals'][deal_id] = {}
                    if not s[city][site]['deals'][deal_id].has_key(node.tag):
                        s[city][site]['deals'][deal_id][node.tag] = node.text
    
    print('Parsing Is Finished')
    print('')

if __name__ == '__main__':
    fetch_data()

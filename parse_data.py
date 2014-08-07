import xml.etree.ElementTree as ET
import os
import sys
import pickle
import cfg

def parse_data(filename):
	keywords = []
	if os.path.isfile(filename):
		tree = ET.parse(filename)
		root_node = tree.getroot()
		for data_node in root_node.iter('data'):
			deal_node = data_node.find('deal')
			keywords.append(deal_node.find('deal_name').text)
			keywords.append(deal_node.find('deal_title').text)
		return keywords
	else:
		print('Not Found file: '+filename)
		return None

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print('''
Usage:
	python parse_data.py --base-dir="data/hangzhou" data.xml+ keywords.txt 
			''')
		sys.exit()
	
	base_dir = sys.argv[1].split('=')[1]
	if os.path.exists(base_dir) is not True:
		print('you lost --base-dir(the first argument)')
		sys.exit()

	keywords_filename = sys.argv[-1]
	if keywords_filename.endswith('.txt') is not True:
		print('you should store result to a .txt file') 
		sys.exit()
	keywords_filename = cfg.datadir+os.sep+keywords_filename
	print('Starting parse data...')

	f = open(keywords_filename, 'a+')
	for datafile in sys.argv[2:-1]:
		datafile = base_dir+os.sep+datafile
		keywords = parse_data(datafile)
		pickle.dump(keywords, f)
	f.close()
	print('Ok! Parse Data is successully!')
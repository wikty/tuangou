import xml.etree.ElementTree as ET
def reduce_data(ofilename, nfilename):
	hold_fields = ['city_name', 'city_id', 'city_url', 'deal_name', 'deal_id', 'deal_title', 'deal_cate', 'deal_subcate', 'deal_url', 'deal_img', 'deal_desc', 'start_time', 'end_time', 'deal_tips']
	tree = ET.parse(ofilename)
	root_node = tree.getroot()
	for data_node in root_node.iter('data'):
		for data_child in data_node:
			if data_child.tag == 'deal':
				for deal_child in data_child:
					print(deal_child.tag,'*')
					if hold_fields.count(deal_child.tag) == 0:
						data_child.remove(deal_child)
			else:
				data_node.remove(data_child)
	tree.write(nfilename, encoding='utf-8', xml_declaration=True)

reduce_data('demo.xml','demo.reduce.xml')
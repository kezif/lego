from bs4 import BeautifulSoup
from config import item_condition_table_inv, color_dict
import re
import csv

def write_item2csv(items, path):
	with open(path,'w') as file:
		attrs = ['part_id','color_id','qty','price','wanted qty', 'condition','name']
		dict_w = csv.DictWriter(file, attrs, delimiter='`')
		dict_w.writeheader()
		dict_w.writerows(items)
		
	
def excract_item_data(html_item):
	
	data = {}
	attrs = [i.text for i in html_item.find_all('strong')]
	
	if not attrs[4].startswith('$'):
		us_price = html_item.find_all('p')[4].text
		price = float(re.findall(r'\$(.*?)\)',us_price)[0])  # everything inside $____)
	else:
		price = float(attrs[4][4:]) # string slicing works just fine..
		
	span_data = [i.text for i in html_item.find_all('span')]
	wanted_qty = int(span_data[-3].split(':')[1])	# "wanted qty: 3" slicing to two parts 
	part_id = html_item.find_all('a', {'class':'link-internal'})[-1].text
	condition = item_condition_table_inv[attrs[0].lower()]		
		
	data['name'] = attrs[2]
	data['color_id']= color_dict[attrs[1].replace(u'\xa0','')]
	data['qty']  = attrs[3]
	data['price'] = price
	data['wanted qty'] = wanted_qty
	data['part_id'] = part_id
	data['condition'] = condition
	return data
	
	
def read_items_fromhtml(path):
	soup = None
	with open(path, 'r') as file:
		soup = BeautifulSoup(file, 'html.parser')
		
	items_html = soup.find_all('article')
	
	items = []
	for item in items_html:
		items.append(excract_item_data(item))
	return items

import os
if __name__ == '__main__':
	#path = r"pages/gritts/page_1_gritts_['mecjh', 'frame+armored', 'mixels parts', 'parta essentials'].html"
	for root, dirs, files in os.walk('pages/mecj_fram_mixe_part'):
		#print(root, dirs, files)
		items = []
		for file in files:
			path = os.path.join(root,file)

			if file.endswith('.html'):
				print(path)
				items.extend(read_items_fromhtml(path))
		write_item2csv(items, os.path.join(root,root.split('/')[-1]+'.csv'))
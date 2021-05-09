from bs4 import BeautifulSoup
from bson.objectid import ObjectId
from pymongo import MongoClient
import pymongo
import requests


def neer_DB():
	cluster = MongoClient('mongodb://localhost:27017/vrem_reduceri_db')
	db = cluster['vrem_reduceri_db']
	collection = db['neer_products']

	all_links = [
		'https://www.neer.ro/sitemap_products_1.xml?from=1481364275242&to=1701673861162',
		'https://www.neer.ro/sitemap_products_2.xml?from=1701674221610&to=1790221287466',
		'https://www.neer.ro/sitemap_products_3.xml?from=1790228496426&to=1925571641386',
		'https://www.neer.ro/sitemap_products_4.xml?from=1925572132906&to=4184377163829',
		'https://www.neer.ro/sitemap_products_5.xml?from=4184377917493&to=4513289371701',
		'https://www.neer.ro/sitemap_products_6.xml?from=4513289732149&to=4547022979125'
	]

	for text in all_links:
		URL = text
		shop = URL.split('/')[2].split('.')[1]
		page = requests.get(URL)
		soup = BeautifulSoup(page.content, 'html.parser')
		available_data = soup.find_all('loc')
		links = [item.get_text() for item in available_data]

		for link in links:
			try:
				web_page = requests.get(link)
				web_soup = BeautifulSoup(web_page.content, 'html.parser')
				schemaorg_data = web_soup.find_all(itemprop=True)
				data = {}
				data['_id'] = ObjectId()

				for item in schemaorg_data:
					if item.get('itemprop') == 'name':
						data[item.get('itemprop')] = item.get_text().strip()
						data['slug'] = item.get_text().strip().lower().replace('"', '').replace(',', '').replace('.', '-').replace(' ', '-')

					if item.get('itemprop') == 'priceCurrency' or item.get('itemprop') == 'price':
						data[item.get('itemprop')] = item.get('content')

					if item.get('itemprop') == 'availability':
						data[item.get('itemprop')] = item.get('href').split('/')[-1]

					if item.get('itemprop') == 'image':
						data[item.get('itemprop')] = 'https:' + item.get('content')

				data['url'] = link
				data['shop'] = shop

				if len(data) > 5:
					result = collection.find_one({'name': data['name']})

					if result == None:
						# print('Insert', link)
						collection.insert_one(data)
					else:
						# print('Update', link)
						data['_id'] = result['_id']
						collection.replace_one({'name': data['name']}, data)

			except:
				print(link)

		# for item in data:
		# 	print(item, ':', data[item])

	print('neer_DB')


if __name__ == '__main__':
	neer_DB()

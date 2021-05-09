from bs4 import BeautifulSoup
from bson.objectid import ObjectId
from pymongo import MongoClient
import pymongo
import requests


def lensa_DB():
	cluster = MongoClient('mongodb://localhost:27017/vrem_reduceri_db')
	db = cluster['vrem_reduceri_db']
	collection = db['lensa_products']

	URL = 'https://www.lensa.ro/sitemap.xml'
	shop = URL.split('/')[2].split('.')[1]
	page = requests.get(URL)
	soup = BeautifulSoup(page.content, 'html.parser')
	available_data = soup.find_all('loc')
	links = [item.get_text() for item in available_data]

	for link in links[197:]:
		try:
			web_page = requests.get(link)
			web_soup = BeautifulSoup(web_page.content, 'html.parser')
			schemaorg_data = web_soup.find_all(itemprop=True)
			data = {}
			data['_id'] = ObjectId()
			exists_name = False
			exists_image = False

			for item in schemaorg_data:
				if item.get('itemprop') == 'name' and exists_name == False:
					data[item.get('itemprop')] = item.get_text().strip()
					exists_name = True
					data['slug'] = item.get_text().strip().lower().replace('"', '').replace(',', '').replace('.', '-').replace(' ', '-')

				if item.get('itemprop') == 'priceCurrency' or item.get('itemprop') == 'price' or item.get('itemprop') == 'sku':
					data[item.get('itemprop')] = item.get('content')

				if item.get('itemprop') == 'brand' or item.get('itemprop') == 'model':
					data[item.get('itemprop')] = item.get_text()

				if item.get('itemprop') == 'identifier':
					data['mpn'] = item.get('content')[4:]

				if item.get('itemprop') == 'availability':
					data[item.get('itemprop')] = item.get('content').split('/')[-1]

				if item.get('itemprop') == 'image' and exists_image == False:
					data[item.get('itemprop')] = item.get('src')
					exists_image = True

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

	print('lensa_DB')


if __name__ == '__main__':
	lensa_DB()
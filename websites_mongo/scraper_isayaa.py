from bs4 import BeautifulSoup
from bson.objectid import ObjectId
from pymongo import MongoClient
import pymongo
import requests


def isayaa_DB():
	cluster = MongoClient('mongodb://localhost:27017/vrem_reduceri_db')
	db = cluster['vrem_reduceri_db']
	collection = db['isayaa_products']

	URL = 'https://www.isayaa.ro/sitemap_products_1.xml?from=3436165824592&to=3640739037264'
	shop = URL.split('/')[2].split('.')[1]
	page = requests.get(URL)
	soup = BeautifulSoup(page.content, 'html.parser')
	available_data = soup.find_all('loc')
	links = [item.get_text() for item in available_data]

	for link in links[1:]:
		try:
			web_page = requests.get(link)
			web_soup = BeautifulSoup(web_page.content, 'html.parser')
			schemaorg_data = web_soup.find_all(itemprop=True)
			data = {}
			data['_id'] = ObjectId()
			exists_image = False

			for item in schemaorg_data:
				if item.get('itemprop') == 'name':
					data[item.get('itemprop')] = item.get('content')
					data['slug'] = item.get('content').lower().replace('"', '').replace(',', '').replace('.', '-').replace(' ', '-')

				if item.get('itemprop') == 'brand' or item.get('itemprop') == 'image' or item.get('itemprop') == 'price' or item.get('itemprop') == 'priceCurrency':
					data[item.get('itemprop')] = item.get('content')

				if item.get('itemprop') == 'availability':
					data[item.get('itemprop')] = item.get('href').split('/')[-1]

			data['url'] = link
			data['shop'] = shop

			print(len(data))
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

	print('isayaa_DB')


if __name__ == '__main__':
	isayaa_DB()

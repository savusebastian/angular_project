from bs4 import BeautifulSoup
from bson.objectid import ObjectId
from pymongo import MongoClient
import pymongo
import requests

# Cant get name
# requests.exceptions.SSLError: HTTPSConnectionPool(host='www.colorcosmetics.ro', port=443): Max retries exceeded with url: /sitemap.xml (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self signed certificate (_ssl.c:1076)')))

def colorcosmetics_DB():
	cluster = MongoClient('mongodb://localhost:27017/vrem_reduceri_db')
	db = cluster['vrem_reduceri_db']
	collection = db['colorcosmetics_products']

	URL = 'https://www.colorcosmetics.ro/sitemap.xml'
	shop = URL.split('/')[2].split('.')[1]
	page = requests.get(URL)
	soup = BeautifulSoup(page.content, 'html.parser')
	available_data = soup.find_all('loc')
	links = [item.get_text() for item in available_data]

	for link in links[50:]:
		try:
			web_page = requests.get(link)
			web_soup = BeautifulSoup(web_page.content, 'html.parser')
			schemaorg_data = web_soup.find_all(itemprop=True)
			data = {}
			data['_id'] = ObjectId()

			for item in schemaorg_data:
				if item.get('itemprop') == 'priceCurrency' or item.get('itemprop') == 'price':
					data[item.get('itemprop')] = item.get_text()

				if item.get('itemprop') == 'image':
					data[item.get('itemprop')] = item.get('content')

			data['url'] = link
			data['shop'] = shop

			print(len(data))
			if len(data) > 5:
				result = collection.find_one({'image': data['image']})

				if result == None:
					# print('Insert', link)
					collection.insert_one(data)
				else:
					# print('Update', link)
					data['_id'] = result['_id']
					collection.replace_one({'image': data['image']}, data)

		except:
			print(link)

	# for item in data:
	# 	print(item, ':', data[item])

	print('colorcosmetics_DB')


if __name__ == '__main__':
	colorcosmetics_DB()

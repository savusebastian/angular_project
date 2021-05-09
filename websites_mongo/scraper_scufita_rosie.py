from bs4 import BeautifulSoup
from bson.objectid import ObjectId
from pymongo import MongoClient
import pymongo
import requests


def scufita_rosie_DB():
	cluster = MongoClient('mongodb://localhost:27017/vrem_reduceri_db')
	db = cluster['vrem_reduceri_db']
	collection = db['scufita_rosie_products']

	URL = 'https://www.scufita-rosie.ro/bauturi-vegetale/5843-naturgreen-biocao-pudra-bio-de-cacao-instant-400g-8437002932923'
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
			exists_name = False
			exists_image = False

			for item in schemaorg_data:
				if item.get('itemprop') == 'name':
					data[item.get('itemprop')] = item.get_text().strip()
					data['slug'] = item.get_text().strip().lower().replace('"', '').replace(',', '').replace('.', '-').replace(' ', '-')

				if item.get('itemprop') == 'brand':
					data[item.get('itemprop')] = item.get_text().strip()

				if item.get('itemprop') == 'priceCurrency' or item.get('itemprop') == 'price' or item.get('itemprop') == 'sku' or item.get('itemprop') == 'availability':
					data[item.get('itemprop')] = item.get('content')

				if item.get('itemprop') == 'image' and exists_image == False:
					data[item.get('itemprop')] = item.get('src')
					exists_image = True

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

	print('scufita_rosie_DB')


if __name__ == '__main__':
	scufita_rosie_DB()

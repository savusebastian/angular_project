from bs4 import BeautifulSoup
from bson.objectid import ObjectId
from pymongo import MongoClient
import pymongo
import requests


def emobili_DB():
	cluster = MongoClient('mongodb://localhost:27017/vrem_reduceri_db')
	db = cluster['vrem_reduceri_db']
	collection = db['emobili_products']

	URL = 'https://www.emobili.ro/cumpara/ban108-divan-canapea-fotoliu-sofa-bancheta-bancuta-cu-lada-banca-1322'
	shop = URL.split('/')[2].split('.')[1]
	page = requests.get(URL)
	soup = BeautifulSoup(page.content, 'html.parser')
	available_data = soup.find_all('loc')
	links = [item.get_text() for item in available_data]

	for link in links:
		try:
			web_page = requests.get(link)
			web_soup = BeautifulSoup(web_page.content, 'html.parser')
			schemaorg_data = web_soup.find_all(type='application/ld+json')[0].contents[0]
			split_data = schemaorg_data.split('"')
			data = {}
			data['_id'] = ObjectId()
			i = 0

			for item in split_data:
				if item == 'name':
					data[item] = split_data[i + 2]
					data['slug'] = split_data[i + 2].lower().replace('"', '').replace(',', '').replace('.', '-').replace(' ', '-')

				if item == 'image' or item == 'mpn' or item == 'priceCurrency':
					data[item] = split_data[i + 2]

				if item == 'price':
					data[item] = split_data[i + 1][1:-1]

				if item == 'brand':
					data[item] = split_data[i + 8]

				if item == 'availability':
					data[item] = split_data[i + 2].split('/')[-1]

				i += 1

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

	print('emobili_DB')


if __name__ == '__main__':
	emobili_DB()

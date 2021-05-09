from bs4 import BeautifulSoup
from bson.objectid import ObjectId
from pymongo import MongoClient
import pymongo
import requests


def inpuff_DB():
	cluster = MongoClient('mongodb://localhost:27017/vrem_reduceri_db')
	db = cluster['vrem_reduceri_db']
	collection = db['inpuff_products']

	URL = 'https://www.inpuff.ro/sitemap_products.xml'
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
			exists_name = False

			for item in split_data:
				if item == 'name' and exists_name == False:
					data[item] = split_data[i + 2]
					exists_name = True
					data['slug'] = split_data[i + 2].lower().replace('"', '').replace(',', '').replace('.', '-').replace(' ', '-')

				if item == 'sku' or item == 'mpn' or item == 'priceCurrency' or item == 'image' or item == 'price':
					data[item] = split_data[i + 2]

				if item == 'brand':
					data[item] = split_data[i + 8]

				if item == 'availability':
					data[item] = split_data[i + 2].split('/')[-1]

				i += 1

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

	print('inpuff_DB')


if __name__ == '__main__':
	inpuff_DB()

from bs4 import BeautifulSoup
from bson.objectid import ObjectId
from pymongo import MongoClient
import pymongo
import requests


def military_shop_DB():
	cluster = MongoClient('mongodb://localhost:27017/vrem_reduceri_db')
	db = cluster['vrem_reduceri_db']
	collection = db['military_shop_products']

	all_links = [
		'https://www.military-shop.ro/sitemap_cat_85.xml',
		'https://www.military-shop.ro/sitemap_cat_67.xml',
		'https://www.military-shop.ro/sitemap_cat_2.xml',
		'https://www.military-shop.ro/sitemap_cat_4.xml',
		'https://www.military-shop.ro/sitemap_cat_101.xml',
		'https://www.military-shop.ro/sitemap_cat_40.xml',
		'https://www.military-shop.ro/sitemap_cat_119.xml',
		'https://www.military-shop.ro/sitemap_cat_37.xml',
		'https://www.military-shop.ro/sitemap_cat_39.xml',
		'https://www.military-shop.ro/sitemap_cat_120.xml',
		'https://www.military-shop.ro/sitemap_cat_147.xml',
		'https://www.military-shop.ro/sitemap_cat_171.xml',
		'https://www.military-shop.ro/sitemap_cat_44.xml',
		'https://www.military-shop.ro/sitemap_cat_35.xml',
		'https://www.military-shop.ro/sitemap_cat_148.xml',
		'https://www.military-shop.ro/sitemap_cat_36.xml',
		'https://www.military-shop.ro/sitemap_cat_141.xml',
		'https://www.military-shop.ro/sitemap_cat_100.xml',
		'https://www.military-shop.ro/sitemap_cat_41.xml',
		'https://www.military-shop.ro/sitemap_cat_38.xml',
		'https://www.military-shop.ro/sitemap_cat_42.xml',
		'https://www.military-shop.ro/sitemap_cat_43.xml',
	]

	for text in all_links:
		URL = text
		shop = URL.split('/')[2].split('.')[1]
		page = requests.get(URL)
		soup = BeautifulSoup(page.content, 'html.parser')
		available_data = soup.find_all('loc')
		links = [item.get_text() for item in available_data]

		for link in links[60:]:
			try:
				web_page = requests.get(link)
				web_soup = BeautifulSoup(web_page.content, 'html.parser')
				schemaorg_data = web_soup.find_all(type='application/ld+json')[0].contents[0]
				split_data = schemaorg_data.split('"')
				data = {}
				data['_id'] = ObjectId()
				i = 0

				for item in split_data:
					if item == 'name' and data[i - 2] == 'Product':
						data[item] = split_data[i + 2]
						data['slug'] = split_data[i + 2].lower().replace('"', '').replace(',', '').replace('.', '-').replace(' ', '-')

					if item == 'image' or item == 'sku' or item == 'priceCurrency':
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

	print('military_shop_DB')


if __name__ == '__main__':
	military_shop_DB()

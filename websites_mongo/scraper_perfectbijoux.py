from bs4 import BeautifulSoup
from bson.objectid import ObjectId
from pymongo import MongoClient
import pymongo
import requests


def perfectbijoux_DB():
	cluster = MongoClient('mongodb://localhost:27017/vrem_reduceri_db')
	db = cluster['vrem_reduceri_db']
	collection = db['perfectbijoux_products']

	all_links = [
		'https://www.perfectbijoux.ro/sitemap_cat_657060.xml',
		'https://www.perfectbijoux.ro/sitemap_cat_436676.xml',
		'https://www.perfectbijoux.ro/sitemap_cat_657073.xml',
		'https://www.perfectbijoux.ro/sitemap_cat_657068.xml',
		'https://www.perfectbijoux.ro/sitemap_cat_657084.xml',
		'https://www.perfectbijoux.ro/sitemap_cat_657108.xml',
		'https://www.perfectbijoux.ro/sitemap_cat_657080.xml',
		'https://www.perfectbijoux.ro/sitemap_cat_657098.xml',
		'https://www.perfectbijoux.ro/sitemap_cat_657096.xml',
	]

	for text in all_links:
		URL = text
		shop = URL.split('/')[2].split('.')[1]
		page = requests.get(URL)
		soup = BeautifulSoup(page.content, 'html.parser')
		available_data = soup.find_all('loc')
		links = [item.get_text() for item in available_data]

		for link in links[40:]:
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
						data['slug'] = split_data[i + 2].strip().lower().replace('"', '').replace(',', '').replace('.', '-').replace(' ', '-')

					if item == 'image' or item == 'sku' or item == 'priceCurrency':
						data[item] = split_data[i + 2]

					if item == 'price':
						data[item] = split_data[i + 1][1:-1]

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

	print('perfectbijoux_DB')


if __name__ == '__main__':
	perfectbijoux_DB()

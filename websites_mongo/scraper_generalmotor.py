from bs4 import BeautifulSoup
from bson.objectid import ObjectId
from pymongo import MongoClient
import pymongo
import requests


def generalmotor_DB():
	cluster = MongoClient('mongodb://localhost:27017/vrem_reduceri_db')
	db = cluster['vrem_reduceri_db']
	collection = db['generalmotor_products']

	all_links = [
		'https://www.generalmotor.ro/sitemap_cat_627696.xml',
		'https://www.generalmotor.ro/sitemap_cat_627605.xml',
		'https://www.generalmotor.ro/sitemap_cat_627510.xml',
		'https://www.generalmotor.ro/sitemap_cat_627673.xml',
		'https://www.generalmotor.ro/sitemap_cat_449471.xml',
		'https://www.generalmotor.ro/sitemap_cat_627556.xml',
		'https://www.generalmotor.ro/sitemap_cat_267923.xml',
		'https://www.generalmotor.ro/sitemap_cat_628239.xml',
		'https://www.generalmotor.ro/sitemap_cat_628238.xml',
		'https://www.generalmotor.ro/sitemap_cat_628240.xml',
		'https://www.generalmotor.ro/sitemap_cat_628237.xml',
		'https://www.generalmotor.ro/sitemap_cat_627636.xml',
		'https://www.generalmotor.ro/sitemap_cat_628241.xml',
		'https://www.generalmotor.ro/sitemap_cat_627674.xml',
		'https://www.generalmotor.ro/sitemap_cat_336878.xml',
		'https://www.generalmotor.ro/sitemap_cat_627593.xml',
		'https://www.generalmotor.ro/sitemap_cat_300509.xml',
		'https://www.generalmotor.ro/sitemap_cat_627691.xml',
		'https://www.generalmotor.ro/sitemap_cat_627527.xml',
		'https://www.generalmotor.ro/sitemap_cat_627682.xml',
		'https://www.generalmotor.ro/sitemap_cat_628247.xml',
		'https://www.generalmotor.ro/sitemap_cat_627853.xml',
		'https://www.generalmotor.ro/sitemap_cat_627703.xml',
		'https://www.generalmotor.ro/sitemap_cat_627681.xml',
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
				schemaorg_data = web_soup.find_all(type='application/ld+json')[0].contents[0]
				split_data = schemaorg_data.split('"')
				data = {}
				data['_id'] = ObjectId()
				i = 0

				for item in split_data:
					if item == 'Product':
						data['name'] = split_data[i + 4]
						data['slug'] = split_data[i + 4].lower().replace('"', '').replace(',', '').replace('.', '-').replace(' ', '-')

					if item == 'sku' or item == 'priceCurrency' or item == 'image':
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

	print('generalmotor_DB')


if __name__ == '__main__':
	generalmotor_DB()

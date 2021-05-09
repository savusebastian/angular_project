from bs4 import BeautifulSoup
from bson.objectid import ObjectId
from pymongo import MongoClient
import pymongo
import requests


def henderson_DB():
	cluster = MongoClient('mongodb://localhost:27017/vrem_reduceri_db')
	db = cluster['vrem_reduceri_db']
	collection = db['henderson_products']

	all_links = [
		'https://henderson.ro/sitemap-product-1.xml',
		'https://henderson.ro/sitemap-product-2.xml',
		'https://henderson.ro/sitemap-product-3.xml',
		'https://henderson.ro/sitemap-product-4.xml',
		'https://henderson.ro/sitemap-product-5.xml',
		'https://henderson.ro/sitemap-product-6.xml',
		'https://henderson.ro/sitemap-product-7.xml',
		'https://henderson.ro/sitemap-product-8.xml',
		'https://henderson.ro/sitemap-product-9.xml',
		'https://henderson.ro/sitemap-product-10.xml',
		'https://henderson.ro/sitemap-product-11.xml',
		'https://henderson.ro/sitemap-product-12.xml',
		'https://henderson.ro/sitemap-product-13.xml',
		'https://henderson.ro/sitemap-product-14.xml',
		'https://henderson.ro/sitemap-product-15.xml',
		'https://henderson.ro/sitemap-product-16.xml',
		'https://henderson.ro/sitemap-product-17.xml',
		'https://henderson.ro/sitemap-product-18.xml',
		'https://henderson.ro/sitemap-product-19.xml',
		'https://henderson.ro/sitemap-product-20.xml',
		'https://henderson.ro/sitemap-product-21.xml',
		'https://henderson.ro/sitemap-product-22.xml',
		'https://henderson.ro/sitemap-product-23.xml',
		'https://henderson.ro/sitemap-product-24.xml',
		'https://henderson.ro/sitemap-product-25.xml',
		'https://henderson.ro/sitemap-product-26.xml',
		'https://henderson.ro/sitemap-product-27.xml',
		'https://henderson.ro/sitemap-product-28.xml',
		'https://henderson.ro/sitemap-product-29.xml',
		'https://henderson.ro/sitemap-product-30.xml',
		'https://henderson.ro/sitemap-product-31.xml',
		'https://henderson.ro/sitemap-product-32.xml',
		'https://henderson.ro/sitemap-product-33.xml',
		'https://henderson.ro/sitemap-product-34.xml',
		'https://henderson.ro/sitemap-product-35.xml',
		'https://henderson.ro/sitemap-product-36.xml',
		'https://henderson.ro/sitemap-product-37.xml',
		'https://henderson.ro/sitemap-product-38.xml',
		'https://henderson.ro/sitemap-product-39.xml',
		'https://henderson.ro/sitemap-product-40.xml',
		'https://henderson.ro/sitemap-product-41.xml',
		'https://henderson.ro/sitemap-product-42.xml',
		'https://henderson.ro/sitemap-product-43.xml',
		'https://henderson.ro/sitemap-product-44.xml',
		'https://henderson.ro/sitemap-product-45.xml',
		'https://henderson.ro/sitemap-product-46.xml',
		'https://henderson.ro/sitemap-product-47.xml',
		'https://henderson.ro/sitemap-product-48.xml',
		'https://henderson.ro/sitemap-product-49.xml',
		'https://henderson.ro/sitemap-product-50.xml',
		'https://henderson.ro/sitemap-product-51.xml',
		'https://henderson.ro/sitemap-product-52.xml',
		'https://henderson.ro/sitemap-product-53.xml',
		'https://henderson.ro/sitemap-product-54.xml',
		'https://henderson.ro/sitemap-product-55.xml',
		'https://henderson.ro/sitemap-product-56.xml',
		'https://henderson.ro/sitemap-product-57.xml',
		'https://henderson.ro/sitemap-product-58.xml',
		'https://henderson.ro/sitemap-product-59.xml',
		'https://henderson.ro/sitemap-product-60.xml',
		'https://henderson.ro/sitemap-product-61.xml',
		'https://henderson.ro/sitemap-product-62.xml',
		'https://henderson.ro/sitemap-product-63.xml',
		'https://henderson.ro/sitemap-product-64.xml',
		'https://henderson.ro/sitemap-product-65.xml',
		'https://henderson.ro/sitemap-product-66.xml',
		'https://henderson.ro/sitemap-product-67.xml',
		'https://henderson.ro/sitemap-product-68.xml',
		'https://henderson.ro/sitemap-product-69.xml',
		'https://henderson.ro/sitemap-product-70.xml',
		'https://henderson.ro/sitemap-product-71.xml',
		'https://henderson.ro/sitemap-product-72.xml',
		'https://henderson.ro/sitemap-product-73.xml',
		'https://henderson.ro/sitemap-product-74.xml',
		'https://henderson.ro/sitemap-product-75.xml',
		'https://henderson.ro/sitemap-product-76.xml',
		'https://henderson.ro/sitemap-product-77.xml',
		'https://henderson.ro/sitemap-product-78.xml',
		'https://henderson.ro/sitemap-product-79.xml',
		'https://henderson.ro/sitemap-product-80.xml',
		'https://henderson.ro/sitemap-product-81.xml',
		'https://henderson.ro/sitemap-product-82.xml',
		'https://henderson.ro/sitemap-product-83.xml',
		'https://henderson.ro/sitemap-product-84.xml',
		'https://henderson.ro/sitemap-product-85.xml',
		'https://henderson.ro/sitemap-product-86.xml',
		'https://henderson.ro/sitemap-product-87.xml',
		'https://henderson.ro/sitemap-product-88.xml',
		'https://henderson.ro/sitemap-product-89.xml',
		'https://henderson.ro/sitemap-product-90.xml',
		'https://henderson.ro/sitemap-product-91.xml',
		'https://henderson.ro/sitemap-product-92.xml',
		'https://henderson.ro/sitemap-product-93.xml',
		'https://henderson.ro/sitemap-product-94.xml',
		'https://henderson.ro/sitemap-product-95.xml',
		'https://henderson.ro/sitemap-product-96.xml',
		'https://henderson.ro/sitemap-product-97.xml',
		'https://henderson.ro/sitemap-product-98.xml',
		'https://henderson.ro/sitemap-product-99.xml',
		'https://henderson.ro/sitemap-product-100.xml',
		'https://henderson.ro/sitemap-product-101.xml',
		'https://henderson.ro/sitemap-product-102.xml',
		'https://henderson.ro/sitemap-product-103.xml',
		'https://henderson.ro/sitemap-product-104.xml',
		'https://henderson.ro/sitemap-product-105.xml',
		'https://henderson.ro/sitemap-product-106.xml',
		'https://henderson.ro/sitemap-product-107.xml',
		'https://henderson.ro/sitemap-product-108.xml',
	]

	for text in all_links:
		URL = text
		shop = URL.split('/')[2].split('.')[0]
		page = requests.get(URL)
		soup = BeautifulSoup(page.content, 'html.parser')
		available_data = soup.find_all('loc')
		links = [item.get_text() for item in available_data]

		for link in links:
			try:
				web_page = requests.get(link)
				web_soup = BeautifulSoup(web_page.content, 'html.parser')
				schemaorg_data = web_soup.find_all(type='application/ld+json')[1].contents[0]
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

					if item == 'model' or item == 'priceCurrency' or item == 'image':
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

	print('henderson_DB')


if __name__ == '__main__':
	henderson_DB()

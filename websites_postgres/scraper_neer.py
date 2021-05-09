from bs4 import BeautifulSoup
import psycopg2
import requests


def neer_DB():
	con = psycopg2.connect(
		host='localhost',
		database='postgres',
		user='postgres',
		password='winding1127!'
	)

	cur = con.cursor()

	all_links = [
		'https://www.neer.ro/sitemap_products_1.xml?from=1481364275242&to=1701673861162',
		'https://www.neer.ro/sitemap_products_2.xml?from=1701674221610&to=1790221287466',
		'https://www.neer.ro/sitemap_products_3.xml?from=1790228496426&to=1925571641386',
		'https://www.neer.ro/sitemap_products_4.xml?from=1925572132906&to=4184377163829',
		'https://www.neer.ro/sitemap_products_5.xml?from=4184377917493&to=4513289371701',
		'https://www.neer.ro/sitemap_products_6.xml?from=4513289732149&to=4547022979125'
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
				schemaorg_data = web_soup.find_all(itemprop=True)
				data = {}
				exists_name = False

				for item in schemaorg_data:
					if item.get('itemprop') == 'name' and exists_name == False:
						data[item.get('itemprop')] = item.get('content')
						exists_name = True

					if item.get('itemprop') == 'priceCurrency' or item.get('itemprop') == 'price' or item.get('itemprop') == 'image':
						data[item.get('itemprop')] = item.get('content')

					if item.get('itemprop') == 'availability':
						data[item.get('itemprop')] = item.get('href').split('/')[-1]

				cur.execute("SELECT product_name FROM product WHERE product_name = '%s'" % data['name'])
				result = cur.fetchall()

				if result != []:
					# print('Update', link)
					cur.execute("UPDATE product SET price = '%s' WHERE product_name = '%s'" % (data['price'], data['name']))
					con.commit()

				else:
					# print('Insert', link)
					cur.execute("INSERT INTO product(%s, %s, %s, %s, %s, %s, %s) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % ('url', 'shop', 'product_name', 'image', 'price', 'price_currency', 'availability', link, shop, data['name'], data['image'], data['price'], data['priceCurrency'], data['availability']))
					con.commit()

			except:
				print(link)

			# for item in data:
			#	 print(item, ':', data[item])

	cur.close()
	con.close()


if __name__ == '__main__':
	neer_DB()

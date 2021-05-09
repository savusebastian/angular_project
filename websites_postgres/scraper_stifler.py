from bs4 import BeautifulSoup
import psycopg2
import requests


def stifler_DB():
	con = psycopg2.connect(
		host='localhost',
		database='postgres',
		user='postgres',
		password='winding1127!'
	)

	cur = con.cursor()

	URL = 'https://www.stifler.ro/sitemap-products1.xml'
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

			for item in schemaorg_data:
				if item.get('itemprop') == 'name':
					data[item.get('itemprop')] = item.get_text().strip()

				if item.get('itemprop') == 'price' or item.get('itemprop') == 'mpn':
					data[item.get('itemprop')] = item.get_text()

				if item.get('itemprop') == 'priceCurrency':
					data[item.get('itemprop')] = item.get('content')

				if item.get('itemprop') == 'availability':
					data[item.get('itemprop')] = item.get('content').split('/')[-1]

				if item.get('itemprop') == 'image':
					data[item.get('itemprop')] = item.get('src')

			cur.execute("SELECT mpn FROM product WHERE mpn = '%s'" % data['mpn'])
			result = cur.fetchall()

			if result != []:
				# print('Update', link)
				cur.execute("UPDATE product SET price = '%s' WHERE mpn = '%s'" % (data['price'], data['mpn']))
				con.commit()

			else:
				# print('Insert', link)
				cur.execute("INSERT INTO product(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % ('url', 'shop', 'product_name', 'image', 'brand', 'model', 'sku', 'mpn', 'price', 'price_currency', 'availability', link, shop, data['name'], data['image'], data['mpn'], data['price'], data['priceCurrency'], data['availability']))
				con.commit()

		except:
			print(link)

		# for item in data:
		#	 print(item, ':', data[item])

	cur.close()
	con.close()


if __name__ == '__main__':
	stifler_DB()

from bs4 import BeautifulSoup
import psycopg2
import requests


def kinghoff_DB():
	con = psycopg2.connect(
		host='localhost',
		database='postgres',
		user='postgres',
		password='winding1127!'
	)

	cur = con.cursor()

	URL = 'http://www.kinghoff.ro/cumpara/infuzor-din-inox-pentru-ceai-sau-cafea-kinghoff-capacitate-350-ml-172'
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
			exists_image = False

			for item in schemaorg_data:
				if item.get('itemprop') == 'name' or item.get('itemprop') == 'brand':
					data[item.get('itemprop')] = item.get_text().strip()

				if item.get('itemprop') == 'priceCurrency' or item.get('itemprop') == 'sku' or item.get('itemprop') == 'price':
					data[item.get('itemprop')] = item.get('content')

				if item.get('itemprop') == 'image' and exists_image == False:
					data[item.get('itemprop')] = item.get('src')
					exists_image = True

			cur.execute("SELECT sku FROM product WHERE sku = '%s'" % data['sku'])
			result = cur.fetchall()

			if result != []:
				# print('Update', link)
				cur.execute("UPDATE product SET price = '%s' WHERE sku = '%s'" % (data['price'], data['sku']))
				con.commit()

			else:
				# print('Insert', link)
				cur.execute("INSERT INTO product(%s, %s, %s, %s, %s, %s, %s, %s) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % ('url', 'shop', 'product_name', 'image', 'brand', 'sku', 'price', 'price_currency', link, shop, data['name'], data['image'], data['brand'], data['sku'], data['price'], data['priceCurrency']))
				con.commit()

		except:
			print(link)

		# for item in data:
		#	 print(item, ':', data[item])

	cur.close()
	con.close()


if __name__ == '__main__':
	kinghoff_DB()

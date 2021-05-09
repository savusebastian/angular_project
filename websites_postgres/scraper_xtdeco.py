from bs4 import BeautifulSoup
import psycopg2
import requests


def xtdeco_DB():
	con = psycopg2.connect(
		host='localhost',
		database='postgres',
		user='postgres',
		password='winding1127!'
	)

	cur = con.cursor()

	URL = 'https://xtdeco.ro/iluminat/aplice/aplic%C4%83-techno-gri-de-markt-717020501'
	shop = URL.split('/')[2].split('.')[1]
	page = requests.get(URL)
	soup = BeautifulSoup(page.content, 'html.parser')
	available_data = soup.find_all('loc')
	links = [item.get_text() for item in available_data]

	for link in links:
		try:
			web_page = requests.get(link)
			web_soup = BeautifulSoup(web_page.content, 'html.parser')
			schemaorg_data = web_soup.find_all(type='application/ld+json')[1].get_text()
			split_data = schemaorg_data.split('"')
			data = {}
			i = 0
			exists_name = False

			for item in split_data:
				if item == 'name' and exists_name == False:
					data[item] = split_data[i + 2]
					exists_name = True

				if item == 'image' or item == 'mpn' or item == 'model' or item == 'priceCurrency' or item == 'brand':
					data[item] = split_data[i + 2]

				if item == 'price':
					data[item] = split_data[i + 1][1:-1]

				if item == 'availability':
					data[item] = split_data[i + 2].split('/')[-1]

				i += 1

			cur.execute("SELECT mpn FROM product WHERE mpn = '%s'" % data['mpn'])
			result = cur.fetchall()

			if result != []:
				# print('Update', link)
				cur.execute("UPDATE product SET price = '%s' WHERE mpn = '%s'" % (data['price'], data['mpn']))
				con.commit()

			else:
				# print('Insert', link)
				cur.execute("INSERT INTO product(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % ('url', 'shop', 'product_name', 'image', 'brand', 'model', 'sku', 'mpn', 'price', 'price_currency', 'availability', link, shop, data['name'], data['image'], data['brand'], data['model'], data['sku'], data['mpn'], data['price'], data['priceCurrency'], data['availability']))
				con.commit()

		except:
			print(link)

		# for item in data:
		#	 print(item, ':', data[item])

	cur.close()
	con.close()


if __name__ == '__main__':
	xtdeco_DB()

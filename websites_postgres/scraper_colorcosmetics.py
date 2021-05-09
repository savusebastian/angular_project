from bs4 import BeautifulSoup
import psycopg2
import requests

# Cant get name
# requests.exceptions.SSLError: HTTPSConnectionPool(host='www.colorcosmetics.ro', port=443): Max retries exceeded with url: /sitemap.xml (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self signed certificate (_ssl.c:1076)')))

def colorcosmetics_DB():
	con = psycopg2.connect(
		host='localhost',
		database='postgres',
		user='postgres',
		password='winding1127!'
	)

	cur = con.cursor()

	URL = 'https://www.colorcosmetics.ro/sitemap.xml'
	shop = URL.split('/')[2].split('.')[1]
	page = requests.get(URL)
	soup = BeautifulSoup(page.content, 'html.parser')
	available_data = soup.find_all('loc')
	links = [item.get_text() for item in available_data]

	for link in links[50:]:
		try:
			web_page = requests.get(link)
			web_soup = BeautifulSoup(web_page.content, 'html.parser')
			schemaorg_data = web_soup.find_all(itemprop=True)
			data = {}

			for item in schemaorg_data:
				if item.get('itemprop') == 'priceCurrency' or item.get('itemprop') == 'price':
					data[item.get('itemprop')] = item.get_text()

				if item.get('itemprop') == 'image':
					data[item.get('itemprop')] = item.get('content')

			cur.execute("SELECT image FROM product WHERE image = '%s'" % data['image'])
			result = cur.fetchall()

			if result != []:
				# print('Update', link)
				cur.execute("UPDATE product SET price = '%s' WHERE image = '%s'" % (data['price'], data['image']))
				con.commit()

			else:
				# print('Insert', link)
				cur.execute("INSERT INTO product(%s, %s, %s, %s, %s, %s) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % ('url', 'shop', 'product_name', 'image', 'price', 'price_currency', link, shop, data['name'], data['image'], data['price'], data['priceCurrency']))
				con.commit()

		except:
			print(link)

		# for item in data:
		#	 print(item, ':', data[item])

	cur.close()
	con.close()


if __name__ == '__main__':
	colorcosmetics_DB()

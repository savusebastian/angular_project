from bs4 import BeautifulSoup
import psycopg2
import requests


def gadgetway_DB():
	con = psycopg2.connect(
		host='localhost',
		database='postgres',
		user='postgres',
		password='winding1127!'
	)

	cur = con.cursor()

	URL = 'http://www.gadgetway.ro/smart-home/448-bec-inteligent-led-cu-bluetooth-veho-kasa-lumina-multicolora-rgb.html'
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
			exists_image = False
			exists_availabilty = False

			for item in schemaorg_data:
				if item.get('itemprop') == 'name' and exists_name == False:
					data[item.get('itemprop')] = item.get_text().strip()
					exists_name = True

				if item.get('itemprop') == 'brand' or item.get('itemprop') == 'price':
					data[item.get('itemprop')] = item.get_text().strip()

				if item.get('itemprop') == 'priceCurrency':
					data[item.get('itemprop')] = item.get('content')

				if item.get('itemprop') == 'availability' and exists_availabilty == False:
					data[item.get('itemprop')] = item.get('href').split('/')[-1]
					exists_availabilty = True

				if item.get('itemprop') == 'image' and exists_image == False:
					data[item.get('itemprop')] = item.get('src')
					exists_image = True

			cur.execute("SELECT product_name FROM product WHERE product_name = '%s'" % data['name'])
			result = cur.fetchall()

			if result != []:
				# print('Update', link)
				cur.execute("UPDATE product SET price = '%s' WHERE product_name = '%s'" % (data['price'], data['name']))
				con.commit()

			else:
				# print('Insert', link)
				cur.execute("INSERT INTO product(%s, %s, %s, %s, %s, %s, %s, %s) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % ('url', 'shop', 'product_name', 'image', 'brand', 'price', 'price_currency', 'availability', link, shop, data['name'], data['image'], data['brand'], data['price'], data['priceCurrency'], data['availability']))
				con.commit()

		except:
			print(link)

		# for item in data:
		#	 print(item, ':', data[item])

	cur.close()
	con.close()


if __name__ == '__main__':
	gadgetway_DB()
